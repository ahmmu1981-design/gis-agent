from __future__ import annotations

from typing import Any, Dict

from geoagent import GeoAgentContext, create_agent

from backend.app.agent.model_provider import build_model_config
from backend.app.agent.prompts import build_system_prompt
from backend.app.agent.tools import build_gis_tools
from backend.app.arcgis.catalog import CatalogValidator
from backend.app.arcgis.client import ArcGISClient
from backend.app.result_capture import ResultCapture


class AgentFactory:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def build(
        self,
        request_id: str,
        result_capture: ResultCapture,
        catalog: CatalogValidator,
        arcgis_client: ArcGISClient,
        user: Dict[str, Any] | None = None,
        model: Any | None = None,
    ):
        tools = build_gis_tools(
            request_id=request_id,
            result_capture=result_capture,
            catalog=catalog,
            arcgis_client=arcgis_client,
            user=user or {},
        )
        context = GeoAgentContext(metadata={"system_prompt": build_system_prompt()})
        config = build_model_config(
            host=self.config.get("OLLAMA_HOST", "http://ollama:11434"),
            model=self.config.get("OLLAMA_MODEL", "qwen3:8b"),
            temperature=float(self.config.get("MODEL_TEMPERATURE", 0.0)),
        )
        return create_agent(context=context, tools=tools, config=config, model=model)
