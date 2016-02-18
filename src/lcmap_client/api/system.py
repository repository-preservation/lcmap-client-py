import logging

from lcmap_client.api import base, routes


log = logging.getLogger(__name__)

context = routes.system_context


class System(base.APIComponent):
    ""
