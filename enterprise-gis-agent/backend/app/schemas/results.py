from pydantic import BaseModel, Field


class ResultRecord(BaseModel):
    catalog_id: str
    feature_count: int = 0
    truncated: bool = False
    geojson: dict = Field(default_factory=dict)
    answer: str = ""
