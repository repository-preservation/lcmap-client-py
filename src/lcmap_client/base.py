import logging

from requests import Request

from lcmap_client import auth, http, logger, models, url
from lcmap_client.config import Config


log = logging.getLogger(__name__)
context = url.base_context


class BaseClient(object):
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
