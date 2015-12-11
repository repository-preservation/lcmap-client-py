import logging

from lcmap_client.models import base, sample_os_process


log = logging.getLogger(__name__)


class Samples(base.Sample):

    def initialize(self):
        self.os_process = sample_os_process.OSProcess(self.http)


class Models(base.Sample):

    def initialize(self):
        self.samples = Samples(self.http)
