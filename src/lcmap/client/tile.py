import base64
import logging

import numpy as np
import numpy.ma as ma

from lcmap.client import geom


log = logging.getLogger(__name__)

# XXX Define more types
gdal_numpy_mapping = {
    'INT16': np.int16,
    'UINT8': np.uint8
}


def decode(spec, result):
    """Create masked numpy array from the encoded data in a tile query's HTTP
    results."""
    t = gdal_numpy_mapping[spec['data_type']]
    s = base64.b64decode(result['data'])
    a = np.frombuffer(s, dtype=t)

    log.debug("decoding {ubid}:{x},{y}".format(**result))

    if spec['data_fill']:
        log.debug("masking fill: {}".format(spec['data_fill']))
        a = ma.masked_equal(a, spec['data_fill'])
    if spec['data_range']:
        v1, v2 = result['data_range']
        log.debug("masking range: {}".format(spec['data_range']))
        a = ma.masked_outside(a, v1, v2)
    if spec['data_shape']:
        log.debug("shaping: {}".format(spec['data_shape']))
        a = a.reshape(spec['data_shape'])
    if spec['data_scale']:
        log.debug("scaling: {}".format(spec['data_scale']))
        a = a * spec['data_scale']

    return a


class Tile(object):

    def __init__(self, tile, spec):
        self._tile = tile
        self._spec = spec
        self._data = decode(spec, tile)
        self._point_transformer = geom.get_transform_matrix(self, spec)
        pass

    @property
    def data(self):
        return self._data

    @property
    def spec(self):
        return self._spec

    @property
    def x(self):
        return int(self._tile['x'])

    @property
    def y(self):
        return int(self._tile['y'])

    @property
    def ubid(self):
        return self._tile['ubid']

    @property
    def acquired(self):
        return self._tile['acquired']

    @property
    def source(self):
        return self._tile['source']

    def __getitem__(self, proj_point):
        """Get value for given projection point"""
        # XXX why isn't this next line using the self._point_transformer matrix
        #     that's areadly been created?
        tm = geom.get_transform_matrix(self, self._spec)  # blech
        (x, y) = proj_point
        (tx, ty) = geom.transform_coord(proj_point, tm, src="map", dst="image")
        return self._data[tx, ty]
