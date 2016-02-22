import logging


from lcmap.client import tile
from lcmap.client.api import base, routes


log = logging.getLogger(__name__)

context = routes.data_context + "/surface-reflectance"
tiles_context = context + "/tiles"


class SurfaceReflectance(base.APIComponent):

    def tiles(self, band, x, y, t1, t2):
        "Get spec and tiles for given band, x, y, and times"
        log_msg = "getting tiles ubid: {0}, point: ({1},{2}), time: {3}/{4}"
        log.debug(log_msg.format(band, x, y, t1, t2))
        point = "{0},{1}".format(x, y)
        time = "{0}/{1}".format(t1, t2)
        resp = self.http.get(
                tiles_context,
                params={"band": band, "point": point, "time": time})
        spec = resp.result['spec']
        return (spec, [tile.Tile(t, spec) for t in resp.result['tiles']])

    def rod(self, band, x, y, t1, t2):
        "Get spec and rod for given band, point, x, y and times"
        spec, tiles = self.tiles(band, x, y, t1, t2)
        ubid = spec['ubid']
        time_and_value = [
                {'value': t[x, y],
                 'acquired': t.acquired,
                 'source': t.source, 'ubid':ubid} for t in tiles]
        return (spec, time_and_value)
