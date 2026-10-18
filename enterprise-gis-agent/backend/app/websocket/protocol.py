from __future__ import annotations

from typing import Any, Dict


def validate_message(message: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(message, dict):
        raise ValueError("Message must be a dictionary.")
    msg_type = message.get("type")
    if msg_type not in {"chat", "status", "ping"}:
        raise ValueError(f"Unsupported message type: {msg_type}")
    request_id = message.get("request_id")
    if not request_id or not isinstance(request_id, str):
        raise ValueError("request_id is required and must be a string.")
    if "message" in message and not isinstance(message["message"], str):
        raise ValueError("message must be a string when present.")
    return message
