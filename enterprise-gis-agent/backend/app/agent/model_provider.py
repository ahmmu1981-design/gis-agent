from geoagent import GeoAgentConfig


def build_model_config(host: str, model: str, temperature: float = 0.0) -> GeoAgentConfig:
    """Configure Ollama through GeoAgent's supported provider resolver."""
    return GeoAgentConfig(
        provider="ollama",
        model=model,
        temperature=temperature,
        ollama_host=host,
    )
