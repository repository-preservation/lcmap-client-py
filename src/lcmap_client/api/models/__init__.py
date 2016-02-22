import logging

from lcmap_client.api import base
from lcmap_client.api.models import sample_os_process

log = logging.getLogger(__name__)


class Samples(base.APIComponent):
    "Class that holds all sample models."
    def initialize(self):
        self.os_process = samples.OSProcess(self.http)
        self.piped_processes = samples.PipedProcesses(self.http)
        # XXX Add os_piped_process & os_docker_process


# XXX Currently a placeholder for CCDC; add iniitialize method to set it up
class CCDCModel(base.APIComponent):
    "The CCDC model."


class Models(base.APIComponent):
    "Class that holds all models, both sample models and actual models."
    def initialize(self):
        self.samples = Samples(self.http)
        self.ccdc = CCDCModel(self.http)
