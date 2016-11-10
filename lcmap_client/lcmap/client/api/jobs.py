import logging

from lcmap.client.api import base, routes


log = logging.getLogger(__name__)

context = routes.jobs_context


class Jobs(base.APIComponent):
    ""
