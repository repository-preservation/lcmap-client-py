import logging

from lcmap.client.api import base, routes


log = logging.getLogger(__name__)

context = routes.models_context + "/ndvi"


class NDVI(base.APIComponent):

    def run(self, x, y, t1, t2):
        params = {"x": x, "y": y, "t1": t1, "t2": t2}
        return self.http.post(context, data=params)
