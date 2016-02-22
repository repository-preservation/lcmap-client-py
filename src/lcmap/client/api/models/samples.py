import logging

from lcmap.client.api import base, routes


log = logging.getLogger(__name__)

sample_context = routes.models_context + "/sample"


class OSProcess(base.APIComponent):

    context = sample_context + "/os-process"

    def run(self, year, delay):
        return self.http.post(
            self.context, data={"year": year, "delay": delay})


class DockerProcess(OSProcess):

    context = sample_context + "/docker-process"

    def run(self, year, docker_tag):
        return self.http.post(
            self.context, data={"year": year, "docker-tag": docker_tag})


class PipedProcesses(base.APIComponent):

    context = sample_context + "/piped-processes"

    def run(self, number="", count="", bytes="", words="", lines=""):
        return self.http.post(self.context, data={
            "number": str(number).lower(),
            "count": str(count).lower(),
            "bytes": str(bytes).lower(),
            "words": str(words).lower(),
            "lines": str(lines).lower()})

