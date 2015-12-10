"""
The client module provides the base class for interacting with the LCMAP
service.

BaseClient is comprised of components (instances of other objects) assigned to
attributes on the class. Some of these components represent the high-level
architecture of the LCMAP service itself, while others are supporting components.
"""
import logging

from lcmap_client import base


log = logging.getLogger(__name__)


class Client(base.BaseClient):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
