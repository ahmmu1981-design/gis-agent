from __future__ import annotations

from typing import Any, Dict, List


VALID_GEOMETRY_TYPES = {"Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection"}


def validate_geometry(geometry: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(geometry, dict):
        raise ValueError("Geometry must be a dictionary.")
    geometry_type = geometry.get("type")
    if geometry_type not in VALID_GEOMETRY_TYPES:
        raise ValueError(f"Unsupported geometry type: {geometry_type}")
    coordinates = geometry.get("coordinates")
    if coordinates is None:
        raise ValueError("Geometry is missing coordinates.")
    if geometry_type == "Point" and not isinstance(coordinates, list) or len(coordinates) != 2:
        raise ValueError("Point geometry requires [x, y] coordinates.")
    if geometry_type == "GeometryCollection" and not isinstance(coordinates, list):
        raise ValueError("GeometryCollection requires a list of geometries.")
    return geometry


def geometry_to_geojson(geometry: Any) -> Dict[str, Any]:
    return validate_geometry(geometry)


def safe_feature(feature: Dict[str, Any]) -> Dict[str, Any]:
    if "geometry" not in feature:
        raise ValueError("Feature is missing a geometry.")
    if "properties" not in feature:
        feature["properties"] = {}
    validate_geometry(feature["geometry"])
    return feature
