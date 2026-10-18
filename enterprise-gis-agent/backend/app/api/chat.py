from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    request_id: str | None = None


@router.post("/chat")
def create_chat(request: ChatRequest) -> dict:
    return {
        "request_id": request.request_id or "demo-request",
        "answer": "This endpoint is configured for the GIS agent backend. Connect a real model provider and GIS tool execution to generate live results.",
        "geojson": {"type": "FeatureCollection", "features": []},
        "status": "accepted",
    }
