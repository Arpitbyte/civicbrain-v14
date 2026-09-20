"""GIS Core and Spatial Analysis REST Endpoints (§A14)."""

import json
import logging
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.identity.jwt import (
    CurrentUserClaims,
    get_optional_user_claims,
)
from civicbrain.domain.identity.models import StaffRole, Ward
from civicbrain.domain.intake.models import Incident, IncidentStatus
from civicbrain.infra.database import get_db
from civicbrain.schemas.gis import (
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    IncidentClusterResponse,
)

logger = logging.getLogger("civicbrain.gis")

router = APIRouter(tags=["GIS & Spatial Analysis"])


@router.get(
    "/wards/geojson",
    response_model=GeoJSONFeatureCollection,
    summary="Get administrative ward polygons as RFC 7946 GeoJSON FeatureCollection",
)
async def get_wards_geojson(
    organization_id: uuid.UUID = Query(..., description="Organization UUID"),
    zone_id: uuid.UUID | None = Query(None, description="Optional Zone filter"),
    db: AsyncSession = Depends(get_db),
) -> GeoJSONFeatureCollection:
    """Stream valid RFC 7946 GeoJSON FeatureCollection for administrative ward boundaries."""
    stmt = select(
        Ward.id,
        Ward.ward_number,
        Ward.name,
        Ward.code,
        Ward.zone_id,
        Ward.organization_id,
        func.ST_AsGeoJSON(Ward.geom).label("geom_json"),
    ).where(Ward.organization_id == organization_id)

    if zone_id:
        stmt = stmt.where(Ward.zone_id == zone_id)

    stmt = stmt.order_by(Ward.ward_number.asc())

    res = await db.execute(stmt)
    rows = res.all()

    features: list[GeoJSONFeature] = []
    for r in rows:
        if not r.geom_json:
            continue
        geom_dict = json.loads(r.geom_json)
        features.append(
            GeoJSONFeature(
                type="Feature",
                id=str(r.id),
                geometry=geom_dict,
                properties={
                    "ward_number": r.ward_number,
                    "name": r.name,
                    "code": r.code,
                    "zone_id": str(r.zone_id),
                    "organization_id": str(r.organization_id),
                },
            )
        )

    return GeoJSONFeatureCollection(type="FeatureCollection", features=features)


@router.get(
    "/incidents/geojson",
    response_model=GeoJSONFeatureCollection,
    summary="Get operational incidents as RFC 7946 GeoJSON FeatureCollection with spatial bounding-box filter",
)
async def get_incidents_geojson(
    organization_id: uuid.UUID = Query(..., description="Organization UUID"),
    department_id: uuid.UUID | None = Query(None, description="Filter by department"),
    incident_status: IncidentStatus | None = Query(
        None, alias="status", description="Filter by incident status"
    ),
    bbox: str | None = Query(
        None,
        description="Spatial bounding box filter: min_lon,min_lat,max_lon,max_lat (e.g. 77.5,12.9,77.6,13.0)",
    ),
    claims: CurrentUserClaims | None = Depends(get_optional_user_claims),
    db: AsyncSession = Depends(get_db),
) -> GeoJSONFeatureCollection:
    """Serve active or filtered operational incidents as GeoJSON FeatureCollection.

    Applies privacy-preserving coordinate scrubbing (~50m snap) for unauthenticated
    or citizen requests, while serving exact geometries to verified municipal staff.
    """
    # Check if caller is verified municipal staff of this organization
    is_staff = bool(
        claims and claims.org_id == organization_id and isinstance(claims.role, StaffRole)
    )

    if is_staff:
        geom_expr = func.ST_AsGeoJSON(Incident.geom).label("geom_json")
    else:
        # Spatial privacy scrubbing: 0.0005 deg ~= 55m coordinate snapping
        geom_expr = func.ST_AsGeoJSON(func.ST_SnapToGrid(Incident.geom, 0.0005)).label("geom_json")

    stmt = select(
        Incident.id,
        Incident.organization_id,
        Incident.department_id,
        Incident.ward_id,
        Incident.category_code,
        Incident.status,
        Incident.severity,
        Incident.created_at,
        geom_expr,
    ).where(Incident.organization_id == organization_id)

    if department_id:
        stmt = stmt.where(Incident.department_id == department_id)

    if incident_status:
        stmt = stmt.where(Incident.status == incident_status)

    # Optional spatial bounding-box filtering (using PostGIS ST_MakeEnvelope and spatial index)
    if bbox:
        try:
            parts = [float(p.strip()) for p in bbox.split(",")]
            if len(parts) != 4:
                raise ValueError("BBox must have 4 coordinates")
            min_lon, min_lat, max_lon, max_lat = parts
            if min_lon > max_lon or min_lat > max_lat:
                raise ValueError("Invalid bbox bounds: min must be <= max")

            envelope = func.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
            stmt = stmt.where(func.ST_Intersects(Incident.geom, envelope))
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid bbox parameter: {e!s}. Format must be min_lon,min_lat,max_lon,max_lat",
            ) from e

    stmt = stmt.order_by(Incident.created_at.desc())

    res = await db.execute(stmt)
    rows = res.all()

    features: list[GeoJSONFeature] = []
    for r in rows:
        if not r.geom_json:
            continue
        geom_dict = json.loads(r.geom_json)
        features.append(
            GeoJSONFeature(
                type="Feature",
                id=str(r.id),
                geometry=geom_dict,
                properties={
                    "organization_id": str(r.organization_id),
                    "department_id": str(r.department_id),
                    "ward_id": str(r.ward_id),
                    "category_code": r.category_code,
                    "status": r.status.value if hasattr(r.status, "value") else str(r.status),
                    "severity": r.severity,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                },
            )
        )

    return GeoJSONFeatureCollection(type="FeatureCollection", features=features)


@router.get(
    "/clusters",
    response_model=list[IncidentClusterResponse],
    summary="Get detected defect density hotspots via in-database DBSCAN spatial clustering (§A14)",
)
async def get_clusters(
    organization_id: uuid.UUID = Query(..., description="Organization UUID"),
    department_id: uuid.UUID | None = Query(None, description="Optional Department filter"),
    eps_meters: float = Query(
        100.0,
        ge=10.0,
        le=10000.0,
        description="Clustering distance epsilon in meters (planar approximation)",
    ),
    min_points: int = Query(
        3, ge=2, le=50, description="Minimum incidents required to form a cluster"
    ),
    db: AsyncSession = Depends(get_db),
) -> list[IncidentClusterResponse]:
    """Execute PostGIS ST_ClusterDBSCAN density clustering for civic defect hotspot detection."""
    rpc_stmt = text(
        """
        SELECT cluster_id, incident_count, centroid_geojson, incident_ids
        FROM get_incident_clusters(
            :org_id,
            :dept_id,
            :eps_meters,
            :min_points
        )
        """
    )
    params: dict[str, Any] = {
        "org_id": organization_id,
        "dept_id": department_id,
        "eps_meters": float(eps_meters),
        "min_points": int(min_points),
    }

    res = await db.execute(rpc_stmt, params)
    rows = res.all()

    clusters: list[IncidentClusterResponse] = []
    for r in rows:
        centroid_dict = json.loads(r.centroid_geojson) if r.centroid_geojson else {}
        incident_uuids = [uuid.UUID(str(u)) for u in r.incident_ids]
        clusters.append(
            IncidentClusterResponse(
                cluster_id=r.cluster_id,
                incident_count=r.incident_count,
                centroid=centroid_dict,
                incident_ids=incident_uuids,
            )
        )

    return clusters
