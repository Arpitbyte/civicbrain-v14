"""Unit tests for GIS Core, GeoJSON serialization, and bounding-box validation (§A14)."""

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from civicbrain.main import app
from civicbrain.schemas.gis import GeoJSONFeature, GeoJSONFeatureCollection, IncidentClusterResponse


@pytest.mark.asyncio
async def test_gis_wards_geojson_empty():
    """Verify GET /v1/gis/wards/geojson returns valid RFC 7946 FeatureCollection for empty org."""
    random_org_id = uuid.uuid4()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(f"/v1/gis/wards/geojson?organization_id={random_org_id}")
        assert res.status_code == 200
        data = res.json()
        assert data["type"] == "FeatureCollection"
        assert data["features"] == []
        # Validate through Pydantic schema
        fc = GeoJSONFeatureCollection.model_validate(data)
        assert fc.type == "FeatureCollection"
        assert len(fc.features) == 0


@pytest.mark.asyncio
async def test_gis_incidents_geojson_empty_and_bbox_validation():
    """Verify GET /v1/gis/incidents/geojson validates bounding-box arguments and returns FeatureCollection."""
    random_org_id = uuid.uuid4()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Valid call without bbox
        res = await client.get(f"/v1/gis/incidents/geojson?organization_id={random_org_id}")
        assert res.status_code == 200
        data = res.json()
        assert data["type"] == "FeatureCollection"
        assert data["features"] == []

        # 2. Valid call with valid bbox (min_lon, min_lat, max_lon, max_lat)
        res_bbox = await client.get(
            f"/v1/gis/incidents/geojson?organization_id={random_org_id}&bbox=77.5,12.9,77.6,13.0"
        )
        assert res_bbox.status_code == 200
        assert res_bbox.json()["type"] == "FeatureCollection"

        # 3. Invalid bbox format (too few parts)
        res_bad1 = await client.get(
            f"/v1/gis/incidents/geojson?organization_id={random_org_id}&bbox=77.5,12.9"
        )
        assert res_bad1.status_code == 400
        assert "Invalid bbox" in res_bad1.json()["detail"]

        # 4. Invalid bbox format (non-numeric)
        res_bad2 = await client.get(
            f"/v1/gis/incidents/geojson?organization_id={random_org_id}&bbox=77.5,foo,77.6,13.0"
        )
        assert res_bad2.status_code == 400

        # 5. Invalid bbox format (min > max)
        res_bad3 = await client.get(
            f"/v1/gis/incidents/geojson?organization_id={random_org_id}&bbox=77.6,13.0,77.5,12.9"
        )
        assert res_bad3.status_code == 400


@pytest.mark.asyncio
async def test_gis_clusters_empty_and_param_validation():
    """Verify GET /v1/gis/clusters parameter validation and empty response for non-existent org."""
    random_org_id = uuid.uuid4()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Valid call returns empty list for unused org
        res = await client.get(
            f"/v1/gis/clusters?organization_id={random_org_id}&eps_meters=150.0&min_points=3"
        )
        assert res.status_code == 200
        assert res.json() == []

        # 2. Parameter validation: min_points < 2 rejected
        res_bad_min = await client.get(
            f"/v1/gis/clusters?organization_id={random_org_id}&min_points=1"
        )
        assert res_bad_min.status_code == 422

        # 3. Parameter validation: eps_meters < 10 rejected
        res_bad_eps = await client.get(
            f"/v1/gis/clusters?organization_id={random_org_id}&eps_meters=5.0"
        )
        assert res_bad_eps.status_code == 422


def test_gis_geojson_schema_structures():
    """Verify GeoJSON RFC 7946 serialization models."""
    feat = GeoJSONFeature(
        type="Feature",
        id="f-1",
        geometry={"type": "Point", "coordinates": [77.5946, 12.9716]},
        properties={"severity": 3, "category": "POTHOLE"},
    )
    fc = GeoJSONFeatureCollection(type="FeatureCollection", features=[feat])
    fc_dict = fc.model_dump()
    assert fc_dict["type"] == "FeatureCollection"
    assert len(fc_dict["features"]) == 1
    assert fc_dict["features"][0]["geometry"]["type"] == "Point"

    # Validate Cluster response model
    cluster = IncidentClusterResponse(
        cluster_id=0,
        incident_count=5,
        centroid={"type": "Point", "coordinates": [77.59, 12.97]},
        incident_ids=[uuid.uuid4(), uuid.uuid4()],
    )
    assert cluster.incident_count == 5
    assert len(cluster.incident_ids) == 2
