import logging

from lcmap_client.api import base, routes


log = logging.getLogger(__name__)

sample_context = routes.models_context + "/sample"


class OSProcess(base.APIComponent):

    context = sample_context + "/os-process"

    def run(self, year, delay):
        return self.http.post(self.context, data={"year": year, "delay": delay})


class PipedProcesses(base.APIComponent):

    context = sample_context + "/piped-processes"

    def run(self, number, count, bytes, words, lines):
        return self.http.post(self.context, data={
            "number": number, "count": count, "bytes": bytes, "words": words,
            "lines": lines})
