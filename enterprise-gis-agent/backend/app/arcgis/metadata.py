from __future__ import annotations

from typing import Any, Dict


def safe_metadata(layer: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "catalog_id": layer.get("catalog_id"),
        "title": layer.get("title"),
        "service_path": layer.get("service_path"),
        "layer_id": layer.get("layer_id"),
        "geometry_type": layer.get("geometry_type"),
        "spatial_reference": layer.get("spatial_reference"),
        "approved_output_fields": layer.get("approved_output_fields", []),
        "max_result_count": int(layer.get("max_result_count", 0)),
    }
