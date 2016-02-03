import base64
import logging
import numpy as np
import numpy.ma as ma

from lcmap_client.data import url


log = logging.getLogger(__name__)
context = url.context + "/surface-reflectance/tiles"


# XXX Define more types
gdal_numpy_mapping = {
    'INT16': np.int16,
    'UINT8': np.uint8
}


def decode(result):
    """Create masked numpy array from tile result's encoded data"""
    t = gdal_numpy_mapping[result['data_type']]
    s = base64.b64decode(result['data'])
    a = np.frombuffer(s, dtype=t)

    log.debug("{ubid} {x},{y}".format(**result))

    if result['data_fill']:
        log.debug("data fill: {}".format(result['data_fill']))
        a = ma.masked_equal(a, result['data_fill'])
    if result['data_range']:
        v1, v2 = result['data_range']
        log.debug("data range: {}".format(result['data_range']))
        a = ma.masked_outside(a, v1, v2)
    if result['data_shape']:
        log.debug("data shape: {}".format(result['data_shape']))
        a = a.reshape(result['data_shape'])
    if result['data_scale']:
        log.debug("data scale: {}".format(result['data_scale']))
        a = a * result['data_scale']

    result['array'] = a
    return result


class SurfaceReflectance(object):

    def __init__(self, http):
        self.http = http
        self.initialize()

    def initialize(self):
        pass

    def tiles(self, band, point, time):
        """Get tiles for given band, point, and ISO8601 time range"""
        log.debug("getting tiles ubid: {0}, point: ({1}) time: {2}".format(band, point, time))
        res = self.http.get(context, params = {"band": band, "point": point, "time": time})
        return [decode(r) for r in res.result]
