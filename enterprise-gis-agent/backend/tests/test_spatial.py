from backend.app.spatial.geometry import validate_geometry
from backend.app.spatial.projections import transform_point


def test_validate_geometry_accepts_point():
    geom = {"type": "Point", "coordinates": [45.0, 24.0]}
    assert validate_geometry(geom)["type"] == "Point"


def test_transform_point_round_trip():
    lon, lat = transform_point((10.0, 20.0), "EPSG:4326", "EPSG:3857")
    assert abs(lon) > 0
    assert abs(lat) > 0
