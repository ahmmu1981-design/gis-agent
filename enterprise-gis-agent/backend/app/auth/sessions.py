import time
import uuid
from typing import Dict, Optional


class SessionStore:
    def __init__(self, expiration_seconds: int = 3600):
        self.expiration_seconds = expiration_seconds
        self._sessions: Dict[str, Dict[str, object]] = {}

    def create_session(self, user_id: str) -> str:
        token = str(uuid.uuid4())
        self._sessions[token] = {
            "user_id": user_id,
            "created_at": time.time(),
            "expires_at": time.time() + max(self.expiration_seconds, 0),
        }
        return token

    def get_session(self, token: str) -> Optional[Dict[str, object]]:
        session = self._sessions.get(token)
        if session is None:
            return None
        expires_at = float(session["expires_at"])
        if time.time() >= expires_at:
            del self._sessions[token]
            return None
        return session

    def destroy_session(self, token: str) -> None:
        self._sessions.pop(token, None)
