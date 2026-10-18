from __future__ import annotations

from typing import Dict


def intersection(catalog_id: str, geometry: dict, limit: int = 20) -> Dict[str, object]:
    if not catalog_id:
        raise ValueError("catalog_id is required.")
    return {
        "catalog_id": catalog_id,
        "status": "ok",
        "limit": limit,
        "geojson": {"type": "FeatureCollection", "features": []},
        "geometry": geometry,
    }
