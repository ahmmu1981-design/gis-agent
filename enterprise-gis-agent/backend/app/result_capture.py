from __future__ import annotations

import uuid
from copy import deepcopy
from typing import Any, Dict, List, Optional


class ResultCapture:
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}

    def begin_request(self, request_id: Optional[str] = None) -> str:
        request_id = request_id or str(uuid.uuid4())
        self._storage[request_id] = {"request_id": request_id, "tool_results": [], "geojson": {"type": "FeatureCollection", "features": []}, "answer": "", "status": "started"}
        return request_id

    def add_tool_result(self, request_id: str, result: Dict[str, Any]) -> None:
        container = self._storage.setdefault(request_id, {"request_id": request_id, "tool_results": [], "geojson": {"type": "FeatureCollection", "features": []}, "answer": "", "status": "running"})
        container["tool_results"].append(deepcopy(result))
        features = result.get("geojson", {}).get("features", [])
        if features:
            container["geojson"]["features"].extend(deepcopy(features))

    def set_answer(self, request_id: str, answer: str) -> None:
        self._storage.setdefault(request_id, {"request_id": request_id, "tool_results": [], "geojson": {"type": "FeatureCollection", "features": []}, "answer": "", "status": "running"})["answer"] = answer

    def complete_request(self, request_id: str) -> Dict[str, Any]:
        container = self._storage.get(request_id)
        if container is None:
            raise KeyError(f"No result context for request {request_id}")
        container["status"] = "complete"
        return deepcopy(container)

    def get_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        container = self._storage.get(request_id)
        if container is None:
            return None
        return deepcopy(container)

    def clear_request(self, request_id: str) -> None:
        self._storage.pop(request_id, None)
