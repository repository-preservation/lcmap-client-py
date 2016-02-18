import logging

from lcmap_client.api import base, routes


log = logging.getLogger(__name__)

context = routes.jobs_context


class Jobs(base.APIComponent):
    ""
