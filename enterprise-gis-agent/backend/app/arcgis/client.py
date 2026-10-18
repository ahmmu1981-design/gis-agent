from __future__ import annotations

from typing import Any, Dict, Optional

import httpx


class ArcGISClient:
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout

    def validate_service_path(self, service_path: str, catalog_id: str) -> str:
        if not service_path or catalog_id == "":
            raise ValueError("Service path and catalog_id are required.")
        if any(token in service_path.lower() for token in ["admin", "rest/services", "logout", "token"]):
            raise ValueError(f"Unsupported service path for catalog entry {catalog_id}: {service_path}")
        return service_path

    def query(self, service_path: str, catalog_id: str, fields: Optional[list[str]] = None, filters: Optional[Dict[str, Any]] = None, limit: int = 50) -> Dict[str, Any]:
        self.validate_service_path(service_path, catalog_id)
        payload = {"catalog_id": catalog_id, "fields": fields or [], "filters": filters or {}, "limit": min(limit, 500)}
        # This is a safe mock placeholder; real deployments replace with authenticated ArcGIS REST calls.
        return {"type": "FeatureCollection", "features": [], "count": 0, "catalog_id": catalog_id, "query": payload}

    def request(self, url: str, method: str = "GET", timeout: Optional[float] = None, **kwargs: Any) -> httpx.Response:
        timeout = timeout or self.timeout
        with httpx.Client(timeout=timeout) as client:
            return client.request(method, url, **kwargs)
