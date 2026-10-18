from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class CatalogValidator:
    def __init__(self, catalog_path: str | Path):
        self.catalog_path = Path(catalog_path)

    def load(self) -> Dict[str, Any]:
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Catalog file not found: {self.catalog_path}")

        with self.catalog_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        self.validate(data)
        return data

    def validate(self, catalog: Dict[str, Any]) -> None:
        if "layers" not in catalog or not isinstance(catalog["layers"], list):
            raise ValueError("Catalog must include a 'layers' array.")

        seen_ids = set()
        for idx, layer in enumerate(catalog["layers"]):
            required = [
                "catalog_id",
                "title",
                "service_path",
                "service_type",
                "layer_id",
                "geometry_type",
                "spatial_reference",
                "approved_output_fields",
                "filterable_fields",
                "supported_operations",
                "max_result_count",
            ]
            missing = [field for field in required if field not in layer]
            if missing:
                raise ValueError(f"Layer at index {idx} missing required fields: {missing}")

            catalog_id = str(layer["catalog_id"])
            if catalog_id in seen_ids:
                raise ValueError(f"Duplicate catalog_id detected: {catalog_id}")
            seen_ids.add(catalog_id)

            if not isinstance(layer["approved_output_fields"], list):
                raise ValueError(f"Layer {catalog_id} must have an approved_output_fields list.")
            if not isinstance(layer["filterable_fields"], list):
                raise ValueError(f"Layer {catalog_id} must have a filterable_fields list.")
            if not isinstance(layer["supported_operations"], list):
                raise ValueError(f"Layer {catalog_id} must have a supported_operations list.")
            if int(layer["max_result_count"]) <= 0:
                raise ValueError(f"Layer {catalog_id} must allow a positive max_result_count.")

    def find_by_id(self, catalog_id: str) -> Dict[str, Any]:
        catalog = self.load()
        for layer in catalog["layers"]:
            if layer.get("catalog_id") == catalog_id:
                return layer
        raise KeyError(f"Catalog ID not found: {catalog_id}")

    def get_layer_ids(self) -> List[str]:
        catalog = self.load()
        return [layer["catalog_id"] for layer in catalog["layers"]]
