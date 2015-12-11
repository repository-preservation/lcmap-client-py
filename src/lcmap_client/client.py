"""
The client module provides the class for interacting with the LCMAP service.

The Client class is comprised of components (instances of other objects)
assigned to attributes on the class. Some of these components represent the
high-level architecture of the LCMAP service itself, while others are
supporting components.
"""
import logging

from requests import Request

from lcmap_client import auth, http, jobs, logger, models, url
from lcmap_client.config import Config


log = logging.getLogger(__name__)
context = url.base_context


class Client(object):
    def __init__(self, force_reload=False, colored_logs=True):
        # API components
        self.compatibility = None
        self.data = None
        self.jobs = None
        self.models = None
        self.notifications = None
        self.systen = None
        self.users = None

        # Supporting components
        self.cfg = None
        self.auth = None
        self.http = None

        # Initialization
        self.initialize(force_reload=force_reload, colored_logs=colored_logs)

    def initialize(self, force_reload=False, colored_logs=True):
        log.debug("Initializing client components ...")
        self.configure(force_reload=force_reload, colored_logs=colored_logs)
        self.http = http.HTTP(cfg=self.cfg)
        self.auth = auth.Auth(cfg=self.cfg, http=self.http)
        self.models = models.Models(self.http)

    def configure(self, force_reload=False, colored_logs=True):
        self.cfg = Config(force_reload=force_reload, colored_logs=colored_logs)
        logger.configure(self.cfg)

    def reload(self):
        self.configure(force_reload=True, colored_logs=self.cfg.colored_logs)
