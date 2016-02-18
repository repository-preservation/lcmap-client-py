import logging

from lcmap_client import client


__version__ = "0.1.0"

log = logging.getLogger(__name__)

Client = client.Client
