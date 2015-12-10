import logging

from lcmap_client import url


log = logging.getLogger(__name__)
context = url.base_context + "/models"


class Sample(object):

    def __init__(self, http):
        self.http = http
        self.initialize()

    def initialize(self):
        pass


class OSProcess(Sample):

    def run(self, year, delay):
        return self.http.post(
            context + "/sample/os-process",
            data={"year": year, "delay": delay})


class Samples(Sample):

    def initialize(self):
        self.os_process = OSProcess(self.http)


class Models(Sample):

    def initialize(self):
        self.samples = Samples(self.http)
