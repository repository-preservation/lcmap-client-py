import logging

from lcmap.client.api import base
from lcmap.client.api.data.surface_reflectance import SurfaceReflectance


log = logging.getLogger(__name__)


class Data(base.APIComponent):

    def initialize(self):
        self.surface_reflectance = SurfaceReflectance(self.http)
