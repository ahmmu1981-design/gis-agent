from __future__ import annotations

from typing import Any, Dict


class BaseModelProvider:
    def __init__(self, host: str, model: str, temperature: float = 0.0):
        self.host = host
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        return {"model": self.model, "prompt": prompt, "temperature": self.temperature, "provider": self.__class__.__name__}


class OllamaProvider(BaseModelProvider):
    def __init__(self, host: str, model: str, temperature: float = 0.0):
        super().__init__(host, model, temperature)

    def generate(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        payload = super().generate(prompt, **kwargs)
        payload["host"] = self.host
        return payload
