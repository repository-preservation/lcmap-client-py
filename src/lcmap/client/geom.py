from math import floor, ceil
from collections import namedtuple

GeoAffine = namedtuple('GeoAffine', ['ul_x', 'x_res', 'rot_1', 'ul_y', 'rot_2', 'y_res'])


def _tile_point_to_proj_point(tile_x, tile_y, transform):
    """
    Translate image row, column into map coordinates
    """
    map_x = transform.ul_x + tile_x * transform.x_res + tile_y * transform.rot_1
    map_y = transform.ul_y + tile_x * transform.rot_2 + tile_y * transform.y_res

    return map_x, map_y


def _proj_point_to_tile_point(proj_x, proj_y, transform):
    """
    Translate map coordinates into image coordinates
    Assumes North is up
    """
    col = floor((proj_x - transform.ul_x - transform.ul_y * transform.rot_1) / transform.x_res)
    row = ceil((proj_y - transform.ul_y - transform.ul_x * transform.rot_2) / transform.y_res)
    return int(col), int(row)


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
    """Return Geo Transform matrix for given tile, spec"""
    return GeoAffine(tile['x'], spec['pixel_x'], spec['shift_x'],
                     tile['y'], spec['shift_y'], spec['pixel_y'])
