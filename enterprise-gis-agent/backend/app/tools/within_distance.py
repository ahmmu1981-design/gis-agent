from __future__ import annotations

from typing import Dict


def within_distance(catalog_id: str, latitude: float, longitude: float, distance_km: float, limit: int = 20) -> Dict[str, object]:
    if not catalog_id:
        raise ValueError("catalog_id is required.")
    return {
        "catalog_id": catalog_id,
        "status": "ok",
        "origin": {"latitude": latitude, "longitude": longitude},
        "distance_km": distance_km,
        "limit": limit,
        "geojson": {"type": "FeatureCollection", "features": []},
    }
