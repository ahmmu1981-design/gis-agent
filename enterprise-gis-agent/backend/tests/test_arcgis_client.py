import pytest

from backend.app.arcgis.client import ArcGISClient


def test_rejects_admin_service_paths():
    client = ArcGISClient()
    with pytest.raises(ValueError):
        client.validate_service_path("https://example.com/arcgis/admin/services", "bad")
