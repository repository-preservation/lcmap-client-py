import logging

from lcmap_client.data.surface_reflectance import SurfaceReflectance


log = logging.getLogger(__name__)


class Data(object):

    def __init__(self, http):
        self.http = http
        self.initialize()

    def initialize(self):
        self.surface_reflectance = SurfaceReflectance(self.http)
