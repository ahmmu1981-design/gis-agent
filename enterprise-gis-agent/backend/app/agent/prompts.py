def build_system_prompt() -> str:
    return (
        "You are a GIS assistant. Use only approved catalog layers and validated GIS tools. "
        "Do not invent coordinates, layer names, or URL values. Explain empty results clearly. "
        "Return structured tool inputs and a concise answer."
    )


def build_user_prompt(message: str) -> str:
    return f"User request: {message}\n\nUse approved catalog tools and return evidence-based answers."
