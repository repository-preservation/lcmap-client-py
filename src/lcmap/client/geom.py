from math import floor
from osgeo import gdal


def _tile_point_to_proj_point(tile_x, tile_y, transform):
    "Translate image coordinates into map coordinates"
    map_x = (transform[0] +
             tile_x * transform[1] +
             tile_y * transform[2])
    map_y = (transform[3] +
             tile_x * transform[4] +
             tile_y * transform[5])
    return (map_x, map_y)


def _proj_point_to_tile_point(proj_x, proj_y, transform):
    "Translate map coordinates into image coordinates"
    inv_transform = gdal.InvGeoTransform(transform).pop()
    image_x = (inv_transform[0] +
               proj_x * inv_transform[1] +
               proj_y * inv_transform[2])
    image_y = (inv_transform[3] +
               proj_x * inv_transform[4] +
               proj_y * inv_transform[5])
    return int(floor(image_x)), int(floor(image_y))


def transform_coord(coord, matrix, src="", dst=""):
    """Transform an (x, y) coordinate from one coordinate system to another.

    Given a coordinate, a transformation matrix, a source system and a
    destination system, perform a coordinate transformation. Supported
    transformations are the following:

    * src="image", dst="map"
    * src="map", dst="image"
    """
    if src == "image" and dst == "map":
        xform = _tile_point_to_proj_point
    elif src == "map" and dst == "image":
        xform = _proj_point_to_tile_point
    return xform(coord[0], coord[1], matrix)


def get_transform_matrix(tile, spec):
    ""
    upper_left_map_x, upper_left_map_y = tile.x, tile.y
    pixel_res_meters_x, pixel_res_meters_y = spec['pixel_x'], spec['pixel_y']
    rotation = 0.0
    return [upper_left_map_x, pixel_res_meters_x, rotation,
            upper_left_map_y, rotation, pixel_res_meters_y]
