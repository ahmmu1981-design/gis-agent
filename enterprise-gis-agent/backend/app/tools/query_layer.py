from __future__ import annotations

from typing import Any, Dict


def query_layer(catalog_id: str, filter_: Dict[str, Any] | None = None, limit: int = 50) -> Dict[str, Any]:
    if not catalog_id:
        raise ValueError("catalog_id is required.")
    return {
        "catalog_id": catalog_id,
        "status": "ok",
        "feature_count": 0,
        "truncated": False,
        "geojson": {"type": "FeatureCollection", "features": []},
        "filter": filter_ or {},
        "limit": limit,
    }
