import logging

from lcmap_client import url


log = logging.getLogger(__name__)
context = url.base_context + "/jobs"


class Jobs(object):
    pass
