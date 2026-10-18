import pytest

from backend.app.arcgis.query_builder import build_filter, validate_filter


def test_build_filter_for_safe_attributes():
    expr = build_filter("status", "active", "=")
    assert expr["field"] == "status"
    assert expr["operator"] == "="
    assert expr["value"] == "active"


def test_rejects_sql_injection():
    with pytest.raises(ValueError):
        validate_filter("status = 'active' OR 1=1")

    with pytest.raises(ValueError):
        build_filter("status", "active OR 1=1", "=")
