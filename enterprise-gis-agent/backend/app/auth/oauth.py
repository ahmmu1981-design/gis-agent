from __future__ import annotations

from typing import Any, Dict


def build_oauth_authorization_url(client_id: str, redirect_uri: str, portal_url: str) -> str:
    if not client_id or not redirect_uri or not portal_url:
        raise ValueError("client_id, redirect_uri, and portal_url are required.")
    return f"{portal_url}/oauth2/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"


def validate_oauth_state(state: str) -> bool:
    return bool(state and len(state) >= 8)


def exchange_code_for_token() -> Dict[str, Any]:
    return {"access_token": "example-token", "token_type": "Bearer"}
