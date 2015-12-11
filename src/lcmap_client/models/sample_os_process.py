import logging

from lcmap_client.models import base, url


log = logging.getLogger(__name__)
context = url.context + "/sample/os-process"


class OSProcess(base.Sample):

    def run(self, year, delay):
        return self.http.post(
            context + "/sample/os-process",
            data={"year": year, "delay": delay})
