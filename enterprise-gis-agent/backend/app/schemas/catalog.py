from pydantic import BaseModel, Field


class CatalogLayer(BaseModel):
    catalog_id: str
    title: str
    description: str | None = None
    service_path: str
    service_type: str = "FeatureServer"
    layer_id: int
    geometry_type: str
    spatial_reference: int = 4326
    approved_output_fields: list[str] = Field(default_factory=list)
    filterable_fields: list[str] = Field(default_factory=list)
    supported_operations: list[str] = Field(default_factory=list)
    max_result_count: int = 100


class Catalog(BaseModel):
    layers: list[CatalogLayer]
