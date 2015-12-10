from requests import Request

from lcmap_client import auth, http, logger
from lcmap_client.config import Config


class BaseClient(object):
    def __init__(self, base_context=""):
        # Client attributes
        self.base_context = base_context

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
        self.initialize()

    def initialize(self):
        self.configure()
        self.http = http.HTTP(cfg=self.cfg, base_context=self.base_context)
        self.auth = auth.Auth(cfg=self.cfg, http=self.http)

    def configure(self):
        self.cfg = Config()
        logger.configure(self.cfg)



