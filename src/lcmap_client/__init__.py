from lcmap_client.client import BaseClient
from lcmap_client.http import client_version


__version__ = client_version
context = "/api"


class Client(BaseClient):
    def __init__(self):
        super(Client, self).__init__(base_context=context)
