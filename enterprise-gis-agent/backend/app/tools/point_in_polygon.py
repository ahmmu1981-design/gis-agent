from __future__ import annotations

from typing import Dict


def point_in_polygon(catalog_id: str, latitude: float, longitude: float) -> Dict[str, object]:
    if not catalog_id:
        raise ValueError("catalog_id is required.")
    return {
        "catalog_id": catalog_id,
        "status": "ok",
        "point": {"latitude": latitude, "longitude": longitude},
        "contains": False,
        "geojson": {"type": "FeatureCollection", "features": []},
    }
