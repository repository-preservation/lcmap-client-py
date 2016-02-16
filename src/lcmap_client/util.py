from math import floor
from osgeo import gdal


def tile_point_to_proj_point(tile_x, tile_y, transform):
    """Translate image coordinates into map coordinates"""
    map_x = (transform[0] +
             tile_x * transform[1] +
             tile_y * transform[2])
    map_y = (transform[3] +
             tile_x * transform[4] +
             tile_y * transform[5])
    return (map_x, map_y)


def proj_point_to_tile_point(proj_x, proj_y, transform):
    """Translate map coordinates into image coordinates"""
    inv_transform = gdal.InvGeoTransform(transform)
    image_x = (inv_transform[0] +
               proj_x * inv_transform[1] +
               proj_y * inv_transform[2])
    image_y = (inv_transform[3] +
               proj_x * inv_transform[4] +
               proj_y * inv_transform[5])
    return (int(floor(image_x)), int(floor(image_y)))


def transform_matrix(tile, spec):
    UpperLeftMapX, UpperLeftMapY = tile.x, tile.y
    PixelResolutionMetersX, PixelResolutionMetersY = spec['pixel_x'], spec['pixel_y']
    Rotation = 0.0
    return [UpperLeftMapX, PixelResolutionMetersX, Rotation,
            UpperLeftMapY, Rotation, PixelResolutionMetersY]
