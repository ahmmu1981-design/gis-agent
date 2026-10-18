from __future__ import annotations

from typing import Any, Dict

from geoagent import geo_tool

from backend.app.arcgis.catalog import CatalogValidator
from backend.app.arcgis.client import ArcGISClient
from backend.app.arcgis.metadata import safe_metadata
from backend.app.arcgis.query_builder import build_filter
from backend.app.result_capture import ResultCapture
from backend.app.spatial.geometry import safe_feature


def build_gis_tools(
    *,
    request_id: str,
    result_capture: ResultCapture,
    catalog: CatalogValidator,
    arcgis_client: ArcGISClient,
    user: Dict[str, Any],
) -> list[Any]:
    """Bind approved GIS execution and result capture to one request."""

    @geo_tool(
        category="arcgis",
        description=(
            "Query one approved ArcGIS catalog layer using an optional structured attribute "
            "filter. Only catalog IDs and filter fields supplied by the backend are allowed."
        ),
    )
    def query_approved_layer(
        catalog_id: str,
        filter_field: str = "",
        operator: str = "=",
        filter_value: str = "",
        limit: int = 50,
    ) -> Dict[str, Any]:
        layer = catalog.find_by_id(catalog_id)
        allowed_groups = set(layer.get("allowed_groups", []))
        user_groups = set(user.get("groups", []))
        if allowed_groups and not allowed_groups.intersection(user_groups):
            raise PermissionError("The current user cannot access this catalog layer.")
        if "query" not in layer["supported_operations"]:
            raise PermissionError("Query is not an approved operation for this layer.")

        filters: Dict[str, Any] = {}
        if filter_field:
            if filter_field not in layer["filterable_fields"]:
                raise ValueError("Filter field is not approved for this catalog layer.")
            filters = build_filter(filter_field, filter_value, operator)
        elif filter_value:
            raise ValueError("A filter field is required when a filter value is provided.")

        result_limit = max(1, min(int(limit), int(layer["max_result_count"])))
        raw_result = arcgis_client.query(
            service_path=layer["service_path"],
            catalog_id=catalog_id,
            fields=layer["approved_output_fields"],
            filters=filters,
            limit=result_limit,
        )
        if not isinstance(raw_result, dict):
            raise ValueError("ArcGIS query returned a malformed response.")

        features = raw_result.get("features")
        if not isinstance(features, list):
            raise ValueError("ArcGIS query response did not contain a feature list.")
        validated_features = []
        approved_fields = set(layer["approved_output_fields"])
        for feature in features:
            clean_feature = safe_feature(dict(feature))
            properties = clean_feature.get("properties")
            if not isinstance(properties, dict):
                raise ValueError("ArcGIS feature attributes must be an object.")
            clean_feature["properties"] = {
                key: value for key, value in properties.items() if key in approved_fields
            }
            validated_features.append(clean_feature)

        geojson = {"type": "FeatureCollection", "features": validated_features}
        tool_result = {
            "catalog_id": catalog_id,
            "layer": safe_metadata(layer),
            "status": "ok",
            "feature_count": len(validated_features),
            "truncated": bool(raw_result.get("truncated", False)),
            "geojson": geojson,
        }
        result_capture.add_tool_result(request_id, tool_result)
        return tool_result

    return [query_approved_layer]
