import logging

from lcmap.client.api import base, routes


log = logging.getLogger(__name__)

context = routes.notifications_context


class Notifications(base.APIComponent):
    ""
