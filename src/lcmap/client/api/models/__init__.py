import logging

from lcmap.client.api import base
from lcmap.client.api.models import ccdc, samples


log = logging.getLogger(__name__)


class Samples(base.APIComponent):
    "Class that holds all sample models."
    def initialize(self):
        self.os_process = samples.OSProcess(self.http)
        self.docker_process = samples.DockerProcess(self.http)
        self.piped_processes = samples.PipedProcesses(self.http)


# XXX if we ever need to group multiple CCDC calls, we can do that here:
# class CCDCModels(base.APIComponent):
#     "The CCDC model."
#     def initialize(self):
#         self.ccdc = ccdc.CCDCPipedProcesses(self.http)


class Models(base.APIComponent):
    "Class that holds all models, both sample models and actual models."
    def initialize(self):
        self.samples = Samples(self.http)
        # XXX for the prototype, we're uding piped processes running local to
        # the REST server -- post-prototype, CCDC will run upon Mesos
        self.ccdc = ccdc.CCDCPipedProcesses(self.http)
