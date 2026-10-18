from __future__ import annotations

from typing import Any, Dict


def nearest_features(catalog_id: str, latitude: float, longitude: float, max_distance: float = 1000.0, result_count: int = 10) -> Dict[str, Any]:
    if not catalog_id:
        raise ValueError("catalog_id is required.")
    return {
        "catalog_id": catalog_id,
        "status": "ok",
        "origin": {"latitude": latitude, "longitude": longitude},
        "max_distance": max_distance,
        "result_count": result_count,
        "geojson": {"type": "FeatureCollection", "features": []},
    }
