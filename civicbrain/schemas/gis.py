"""Geospatial and GeoJSON schemas for GIS Core (§A14)."""

import uuid
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class GeoJSONFeature(BaseModel):
    """RFC 7946 GeoJSON Feature representation."""

    model_config = ConfigDict(from_attributes=True)

    type: Literal["Feature"] = "Feature"
    id: str | None = None
    geometry: dict[str, Any]
    properties: dict[str, Any]


class GeoJSONFeatureCollection(BaseModel):
    """RFC 7946 GeoJSON FeatureCollection representation."""

    model_config = ConfigDict(from_attributes=True)

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[GeoJSONFeature]


class IncidentClusterResponse(BaseModel):
    """Detected defect density hotspot cluster (§A14)."""

    model_config = ConfigDict(from_attributes=True)

    cluster_id: int
    incident_count: int
    centroid: dict[str, Any]
    incident_ids: list[uuid.UUID]
