import re
from typing import Any, Dict, Mapping

_UNSAFE_EXPRESSION_RE = re.compile(r"(?is)(;|--|\b(or|union|select|drop|delete|update|insert|alter|truncate)\b)")


def validate_filter(expression: str) -> str:
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Filter expression must be a non-empty string.")
    if _UNSAFE_EXPRESSION_RE.search(expression):
        raise ValueError("Unsafe SQL-like filter expression detected.")
    if expression.count("'") % 2 != 0:
        raise ValueError("Unbalanced string literal in filter expression.")
    return expression.strip()


def validate_identifier(field_name: str) -> str:
    if not isinstance(field_name, str) or not field_name.strip():
        raise ValueError("Field name must be a non-empty string.")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", field_name.strip()):
        raise ValueError(f"Invalid field identifier: {field_name}")
    return field_name.strip()


def build_filter(field_name: str, value: Any, operator: str = "=") -> Dict[str, Any]:
    field = validate_identifier(field_name)
    if isinstance(value, str) and _UNSAFE_EXPRESSION_RE.search(value):
        raise ValueError("Unsafe value provided for filter.")
    if isinstance(value, str) and value.strip() == "":
        raise ValueError("Filter value cannot be empty.")
    allowed_operators = {"=", "!=", ">", "<", ">=", "<=", "LIKE", "IN"}
    if operator.upper() not in allowed_operators:
        raise ValueError(f"Unsupported operator: {operator}")
    return {"field": field, "operator": operator, "value": value}
