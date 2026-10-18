import os
from dataclasses import dataclass
from typing import List


def _read_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class Settings:
    portal_url: str = ""
    arcgis_server_url: str = ""
    arcgis_oauth_client_id: str = ""
    arcgis_oauth_client_secret: str = ""
    arcgis_redirect_uri: str = ""
    ollama_host: str = "http://ollama:11434"
    ollama_model: str = "qwen3:8b"
    model_temperature: float = 0.0
    session_secret: str = "change-me-in-production"
    redis_url: str = "redis://redis:6379/0"
    allowed_origins: str = "*"
    catalog_path: str = "/app/catalog.json"
    log_level: str = "INFO"
    request_timeout_seconds: int = 30
    max_features: int = 500

    @property
    def allowed_origins_list(self) -> List[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]


def load_settings() -> Settings:
    return Settings(
        portal_url=_read_env("PORTAL_URL"),
        arcgis_server_url=_read_env("ARCGIS_SERVER_URL"),
        arcgis_oauth_client_id=_read_env("ARCGIS_OAUTH_CLIENT_ID"),
        arcgis_oauth_client_secret=_read_env("ARCGIS_OAUTH_CLIENT_SECRET"),
        arcgis_redirect_uri=_read_env("ARCGIS_REDIRECT_URI"),
        ollama_host=_read_env("OLLAMA_HOST", "http://ollama:11434"),
        ollama_model=_read_env("OLLAMA_MODEL", "qwen3:8b"),
        model_temperature=float(_read_env("MODEL_TEMPERATURE", "0.0") or "0.0"),
        session_secret=_read_env("SESSION_SECRET", "change-me-in-production"),
        redis_url=_read_env("REDIS_URL", "redis://redis:6379/0"),
        allowed_origins=_read_env("ALLOWED_ORIGINS", "*"),
        catalog_path=_read_env("CATALOG_PATH", "/app/catalog.json"),
        log_level=_read_env("LOG_LEVEL", "INFO"),
        request_timeout_seconds=int(_read_env("REQUEST_TIMEOUT_SECONDS", "30") or "30"),
        max_features=int(_read_env("MAX_FEATURES", "500") or "500"),
    )


def validate_configuration(settings: Settings) -> None:
    if not settings.session_secret or settings.session_secret == "change-me-in-production":
        raise ValueError("SESSION_SECRET must be set to a secure secret value in production.")
    if not settings.catalog_path:
        raise ValueError("CATALOG_PATH is required.")
    if not settings.ollama_host:
        raise ValueError("OLLAMA_HOST is required.")
    if not settings.ollama_model:
        raise ValueError("OLLAMA_MODEL is required.")
