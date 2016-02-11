import base64
import logging
import numpy as np
import numpy.ma as ma

from lcmap_client.data import url


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


class Dice(object):
    
    def __init__(self, response):
        self._source = response.result
        self._spec = response.result['spec']
        self._tiles = [Tile(tile, self._spec) for tile in res.result['tiles']]

    def tiles(self):
        return self._tiles

    def rod(self):
        return []


class Tile(object):

    def __init__(self, tile, spec):
        # We preserve the original tile object because it has useful information...
        # - upper left (x,y) in projection coordinate system
        # - acquisition date
        # - universal band ID
        self._tile = tile
        self._data = decode(spec, tile)
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


class SurfaceReflectance(object):

    def __init__(self, http):
        self.http = http
        self.initialize()

    def initialize(self):
        pass

    def tiles(self, band, point, time):
        """Get tiles for given band, point, and ISO8601 time range"""
        log.debug("getting tiles ubid: {0}, point: ({1}) time: {2}".format(band, point, time))
        response = self.http.get(context + "tiles", params = {"band": band, "point": point, "time": time})
        # Spec contains metadata that describes the location, shape, and type 
        # of data within a projection coordinate system. It is used to decode
        # scale, and mask data.
        spec = response.result['spec']
        return (spec, [Tile(t,spec) for t in response.result['tiles']])

