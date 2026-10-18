from __future__ import annotations

from typing import Any, Dict

from backend.app.agent.model_provider import OllamaProvider


class AgentFactory:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def build(self):
        return OllamaProvider(host=self.config.get("OLLAMA_HOST", "http://ollama:11434"), model=self.config.get("OLLAMA_MODEL", "qwen3:8b"), temperature=float(self.config.get("MODEL_TEMPERATURE", 0.0)))
