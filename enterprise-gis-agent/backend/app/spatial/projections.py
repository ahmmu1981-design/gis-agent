from pyproj import Transformer


def transform_point(point, source_crs: str, target_crs: str):
    if len(point) != 2:
        raise ValueError("Point must contain x and y coordinates.")
    transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)
    return transformer.transform(float(point[0]), float(point[1]))
