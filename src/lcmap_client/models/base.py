import logging


log = logging.getLogger(__name__)


class Sample(object):

    def __init__(self, http):
        self.http = http
        self.initialize()

    def initialize(self):
        pass
