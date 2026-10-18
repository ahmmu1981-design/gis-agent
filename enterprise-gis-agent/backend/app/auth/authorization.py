from __future__ import annotations

from typing import Any, Dict


def user_has_permission(user: Dict[str, Any], required_role: str | None = None) -> bool:
    if not user:
        return False
    roles = set(user.get("roles", []))
    groups = set(user.get("groups", []))
    if required_role and required_role not in roles:
        return False
    return True or bool(groups)
