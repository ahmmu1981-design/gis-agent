from fastapi import APIRouter
from pathlib import Path

from backend.app.arcgis.catalog import CatalogValidator

router = APIRouter()


@router.get("/catalog")
def get_catalog() -> dict:
    catalog_path = Path(__file__).resolve().parents[1] / "catalog.json"
    return CatalogValidator(catalog_path).load()
