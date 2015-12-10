import logging


log = logging.getLogger(__name__)


def Client(*args, **kwargs):
    from lcmap_client.client import Client
    return Client(*args, **kwargs)


def get_version():
    from lcmap_client.http import client_version
    return client_version


__version__ = get_version()

