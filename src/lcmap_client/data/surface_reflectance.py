import base64
import logging
import numpy as np
import numpy.ma as ma

from lcmap_client.data import url
from lcmap_client.geom import proj_point_to_tile_point, transform_matrix


log = logging.getLogger(__name__)
context = url.context + "/surface-reflectance/"


# XXX Define more types
gdal_numpy_mapping = {
    'INT16': np.int16,
    'UINT8': np.uint8
}


def decode(spec, result):
    """Create masked numpy array from tile result's encoded data"""
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
        self._point_transformer = transform_matrix(self, spec)
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
        tm = transform_matrix(self, self._spec)  # blech
        x, y = proj_point
        tx, ty = proj_point_to_tile_point(x, y, tm)
        return self._data[tx, ty]


class SurfaceReflectance(object):

    def __init__(self, http):
        self.http = http
        self.initialize()

    def initialize(self):
        pass

    def tiles(self, band, x, y, t1, t2):
        """Get spec and tiles for given band, x, y, and times"""
        log.debug("getting tiles ubid: {0}, point: ({1},{2}), time: {3}/{4}".format(band, x, y, t1, t2))
        point = "{0},{1}".format(x, y)
        time = "{0}/{1}".format(t1, t2)
        resp = self.http.get(context + "tiles", params={"band": band, "point": point, "time": time})
        spec = resp.result['spec']
        return (spec, [Tile(t, spec) for t in resp.result['tiles']])

    def rod(self, band, x, y, t1, t2):
        """Get spec and rod for given band, point, x, y and times"""
        spec, tiles = self.tiles(band, x, y, t1, t2)
        ubid = spec['ubid']
        time_and_value = [{'value': t[x, y], 'acquired':t.acquired, 'source':t.source, 'ubid':ubid} for t in tiles]
        return spec, time_and_value
