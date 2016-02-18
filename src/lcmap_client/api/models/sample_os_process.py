import logging

from lcmap_client.api import base, routes


log = logging.getLogger(__name__)
context = routes.models_context + "/sample/os-process"


class OSProcess(base.APIComponent):

    def run(self, year, delay):
        return self.http.post(context, data={"year": year, "delay": delay})
