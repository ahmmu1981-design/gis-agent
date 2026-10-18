from pathlib import Path

from backend.app.arcgis.catalog import CatalogValidator


def test_catalog_validates_sample_entries():
    catalog_path = Path(__file__).resolve().parents[1] / "catalog.json"
    validator = CatalogValidator(catalog_path)
    catalog = validator.load()

    assert "layers" in catalog
    assert len(catalog["layers"]) >= 1
    assert all(entry["catalog_id"] for entry in catalog["layers"])
