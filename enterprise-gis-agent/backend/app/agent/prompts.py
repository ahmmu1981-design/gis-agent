def build_system_prompt() -> str:
    return (
        "You are an enterprise GIS assistant. Use only the registered GIS tools and catalog IDs "
        "provided to you. Never invent service URLs, layer IDs, fields, filters, features, or "
        "query results. The backend validates catalog access and executes every GIS request. "
        "Base your answer only on returned tool results, explain empty results, and ask a "
        "clarifying question when a request cannot be mapped safely to an approved layer."
    )


def build_user_prompt(message: str) -> str:
    return f"User request: {message}\n\nUse approved catalog tools and return evidence-based answers."
