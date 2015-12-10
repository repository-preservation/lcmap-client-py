import sys

from requests import Request, Session

import lcmap_client


context = "/api"
server_version = "1.0"
client_version = "0.1.0"
default_endpoint = "http://localhost:8080"
default_content_type = "json"
vendor = "vnd.usgs.lcmap"
project_url = "https://github.com/usgs-eros/lcmap-client-py"
user_agent = "LCMAP REST Client/{} (Python {}) (+{})".format(
    client_version, sys.version.replace("\n", ""), project_url)


def split_media_type(media_type):
    [type, suffix] = media_type.split("/")
    return {"type": type, "suffix": suffix}


def format_accept(vendor, version, content_type):
    media_type = split_media_type(content_type)
    return "{}/{}.v{}+{}".format(
        media_type["type"], vendor, version, media_type["suffix"])


def get_base_headers():
    return {}


class HTTP(object):
    def __init__(self, cfg=None, base_context=""):
        self.cfg = cfg
        self.base_context = base_context
        self.base_url = self.cfg.get_endpoint() + self.base_context
        self.session = Session()
        self.session.headers.update(get_base_headers())

    def request(self, method, path, *args, **kwargs):
        url = self.base_url + path
        req = Request(*([method.upper(), url] + list(args)), **kwargs)
        resp = self.session.send(req.prepare())
        # XXX we'll need to change the following to parse the results based on
        # content type, but right now the server is returning the fairly useless
        # application/octet-stream type, even for JSON
        return resp.json()

    def post(self, path, *args, **kwargs):
        return self.request('POST', path, *args, **kwargs)

    def get(self, path, *args, **kwargs):
        return self.request('GET', path, *args, **kwargs)
