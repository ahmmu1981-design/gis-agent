import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.agent.factory import AgentFactory
from backend.app.arcgis.catalog import CatalogValidator
from backend.app.arcgis.client import ArcGISClient
from backend.app.config import load_settings
from backend.app.result_capture import ResultCapture

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    request_id: str | None = None


def format_chat_response(request_id: str, response, result_capture: ResultCapture) -> dict:
    if not response.success:
        raise HTTPException(status_code=502, detail=response.error_message or "GIS agent failed.")
    answer = response.answer_text or ""
    result_capture.set_answer(request_id, answer)
    captured = result_capture.complete_request(request_id)
    return {
        "request_id": request_id,
        "answer": answer,
        "geojson": captured["geojson"],
        "tool_results": captured["tool_results"],
        "tool_calls": response.tool_calls,
        "status": "complete",
    }


@router.post("/chat")
def create_chat(request: ChatRequest) -> dict:
    request_id = request.request_id or str(uuid.uuid4())
    result_capture = ResultCapture()
    result_capture.begin_request(request_id)
    settings = load_settings()
    catalog_path = Path(__file__).resolve().parents[1] / "catalog.json"
    catalog = CatalogValidator(catalog_path)
    catalog.load()

    config = {
        "OLLAMA_HOST": settings.ollama_host,
        "OLLAMA_MODEL": settings.ollama_model,
        "MODEL_TEMPERATURE": settings.model_temperature,
    }
    agent = AgentFactory(config).build(
        request_id=request_id,
        result_capture=result_capture,
        catalog=catalog,
        arcgis_client=ArcGISClient(timeout=settings.request_timeout_seconds),
    )
    response = agent.chat(request.message)
    return format_chat_response(request_id, response, result_capture)
