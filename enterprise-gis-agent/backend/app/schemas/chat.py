from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    request_id: str | None = None


class ChatResponse(BaseModel):
    request_id: str
    answer: str
    status: str
    geojson: dict
