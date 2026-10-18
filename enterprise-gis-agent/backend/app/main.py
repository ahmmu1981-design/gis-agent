from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.auth import router as auth_router
from backend.app.api.catalog import router as catalog_router
from backend.app.api.chat import router as chat_router
from backend.app.api.health import router as health_router
from backend.app.config import load_settings, validate_configuration
from backend.app.logging_config import configure_logging

settings = load_settings()
validate_configuration(settings)
configure_logging(settings.log_level)

app = FastAPI(title="Enterprise GIS Agent", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list if settings.allowed_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router, prefix="/api")
app.include_router(catalog_router, prefix="/api")
app.include_router(chat_router, prefix="/api")


@app.get("/")
def root() -> dict:
    return {"message": "Enterprise GIS Agent API is running."}
