import logging

from lcmap_client.client import BaseClient
from lcmap_client.http import client_version


__version__ = client_version
log = logging.getLogger(__name__)
context = "/api"


class Client(BaseClient):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(base_context=context, *args, **kwargs)
