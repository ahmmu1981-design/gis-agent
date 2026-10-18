from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from typing import Any

import pytest
from geoagent import GeoAgent
from strands.models.model import Model
from strands.models.ollama import OllamaModel

from backend.app.agent.factory import AgentFactory
from backend.app.api.chat import format_chat_response
from backend.app.arcgis.catalog import CatalogValidator
from backend.app.result_capture import ResultCapture


CATALOG = CatalogValidator(Path(__file__).resolve().parents[1] / "catalog.json")
CONFIG = {
    "OLLAMA_HOST": "http://ollama.invalid:11434",
    "OLLAMA_MODEL": "qwen3:8b",
    "MODEL_TEMPERATURE": 0.0,
}


class SimulatedArcGISClient:
    def __init__(self, feature_name):
        self.feature_name = feature_name
        self.calls = []

    def query(self, **kwargs):
        self.calls.append(kwargs)
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [46.7, 24.7]},
                    "properties": {"OBJECTID": 1, "name": self.feature_name, "status": "active", "unapproved": "hidden"},
                }
            ],
            "truncated": False,
        }


def build_test_agent(request_id, capture, client, user=None, model=None):
    capture.begin_request(request_id)
    return AgentFactory(CONFIG).build(
        request_id=request_id,
        result_capture=capture,
        catalog=CATALOG,
        arcgis_client=client,
        user=user or {},
        model=model,
    )


class SimulatedToolCallModel(Model):
    """Emit Ollama-shaped Strands events without a model service."""

    def __init__(self):
        self.calls = 0

    def update_config(self, **model_config: Any) -> None:
        self.config = model_config

    def get_config(self) -> dict:
        return getattr(self, "config", {})

    async def structured_output(self, output_model, prompt, system_prompt=None, **kwargs):
        if False:
            yield {}

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kwargs):
        self.calls += 1
        if self.calls == 1:
            yield {"messageStart": {"role": "assistant"}}
            yield {"contentBlockStart": {"start": {"toolUse": {"name": "query_approved_layer", "toolUseId": "simulated-call-1"}}}}
            yield {
                "contentBlockDelta": {
                    "delta": {
                        "toolUse": {
                            "input": json.dumps({"catalog_id": "sample_facilities", "limit": 1})
                        }
                    }
                }
            }
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "tool_use"}}
            return

        yield {"messageStart": {"role": "assistant"}}
        yield {"contentBlockStart": {"start": {}}}
        yield {"contentBlockDelta": {"delta": {"text": "The approved query returned one facility named Alpha."}}}
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "end_turn"}}


def test_factory_builds_geoagent_with_ollama_and_registered_tool():
    capture = ResultCapture()
    agent = build_test_agent("request-config", capture, SimulatedArcGISClient("One"))

    assert isinstance(agent, GeoAgent)
    assert agent.config.provider == "ollama"
    assert agent.config.model == "qwen3:8b"
    assert agent.config.temperature == 0.0
    assert agent.config.ollama_host == "http://ollama.invalid:11434"
    assert isinstance(agent.strands_agent.model, OllamaModel)
    assert "query_approved_layer" in agent.tool_names
    assert "registered GIS tools" in agent.context.metadata["system_prompt"]


def test_geoagent_tool_caller_executes_approved_query_and_captures_actual_output():
    capture = ResultCapture()
    client = SimulatedArcGISClient("Actual Feature")
    agent = build_test_agent("request-tool", capture, client)

    agent.tool.query_approved_layer(
        catalog_id="sample_facilities",
        filter_field="status",
        operator="=",
        filter_value="active",
        limit=10,
    )

    stored = capture.get_request("request-tool")
    assert client.calls[0]["catalog_id"] == "sample_facilities"
    assert client.calls[0]["filters"] == {"field": "status", "operator": "=", "value": "active"}
    assert stored["geojson"]["features"][0]["properties"] == {
        "OBJECTID": 1,
        "name": "Actual Feature",
        "status": "active",
    }
    assert stored["tool_results"][0]["geojson"] == stored["geojson"]


def test_simulated_model_tool_call_runs_through_geoagent_chat_loop():
    capture = ResultCapture()
    client = SimulatedArcGISClient("Alpha")
    model = SimulatedToolCallModel()
    agent = build_test_agent("request-model-call", capture, client, model=model)

    response = agent.chat("Find an approved facility")

    assert response.success is True
    assert "one facility named Alpha" in response.answer_text
    assert response.executed_tools == ["query_approved_layer"]
    assert len(client.calls) == 1
    assert capture.get_request("request-model-call")["geojson"]["features"][0]["properties"]["name"] == "Alpha"


def test_response_keeps_geoagent_answer_and_tool_geojson_separate():
    capture = ResultCapture()
    request_id = capture.begin_request("request-response")
    feature_collection = {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2]}, "properties": {"name": "Tool result"}}],
    }
    capture.add_tool_result(request_id, {"catalog_id": "sample_facilities", "geojson": feature_collection})

    class Response:
        success = True
        answer_text = "The approved query returned one feature."
        tool_calls = [{"name": "query_approved_layer"}]

    payload = format_chat_response(request_id, Response(), capture)
    assert payload["answer"] == "The approved query returned one feature."
    assert payload["geojson"] == feature_collection
    assert payload["answer"] != str(payload["geojson"])


def test_concurrent_geoagent_tool_calls_keep_request_results_isolated():
    def run(request_id, feature_name):
        capture = ResultCapture()
        client = SimulatedArcGISClient(feature_name)
        agent = build_test_agent(request_id, capture, client)
        agent.tool.query_approved_layer(catalog_id="sample_facilities", limit=1)
        return capture.complete_request(request_id)

    with ThreadPoolExecutor(max_workers=2) as pool:
        first, second = list(pool.map(lambda args: run(*args), [("request-a", "Alpha"), ("request-b", "Bravo")]))

    assert first["geojson"]["features"][0]["properties"]["name"] == "Alpha"
    assert second["geojson"]["features"][0]["properties"]["name"] == "Bravo"
    assert first["request_id"] == "request-a"
    assert second["request_id"] == "request-b"


def test_tool_rejects_unapproved_layer_before_arcgis_call():
    capture = ResultCapture()
    client = SimulatedArcGISClient("Should not run")
    agent = build_test_agent("request-denied", capture, client)

    result = agent.tool.query_approved_layer(catalog_id="not-approved")

    assert result is not None
    assert client.calls == []
    assert capture.get_request("request-denied")["tool_results"] == []


def test_agent_source_has_no_direct_strands_or_raw_ollama_fallback():
    source_root = Path(__file__).resolve().parents[1] / "app" / "agent"
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_root.glob("*.py"))
    assert "from strands import Agent" not in source
    assert "OllamaProvider" not in source
    assert "ollama.Client" not in source
    assert "httpx.post" not in source
