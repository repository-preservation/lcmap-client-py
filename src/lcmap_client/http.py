"""
The http module contains the primary HTTP class which provides convenience
methods for making calls to the LCMAP service. Supporting module-level
functions are also provided.

The conveniences provided by the HTTP class include:
* session setup
* default headers
* header updates based upon state changes
* path-based requests (as opposed to whole URLs)

"""
import logging
import sys

from requests import Request, Session

import lcmap_client


log = logging.getLogger(__name__)
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
    split = media_type.split("/")
    if len(split) == 1:
        log.debug("Only got one part for the media type: {}".format(split))
        [type, suffix] = ["application", split[0]]
    elif len(split) == 2:
        [type, suffix] = split
    else:
        [type, suffix] = split[:2]
    return {"type": type, "suffix": suffix}


def format_accept(vendor, version, content_type):
    media_type = split_media_type(content_type)
    return "{}/{}.v{}+{}".format(
        media_type["type"], vendor, version, media_type["suffix"])


def get_base_headers():
    return {"User-Agent": user_agent}


def make_headers(version, content_type):
    headers = get_base_headers()
    headers.update(
        {"Accept": format_accept(vendor, version, content_type)})
    return headers


def make_auth_header(api_token):
    return {"X-AuthToken": api_token}


class Response(object):

    def __init__(self, http, response, result, errors):
        self.http = http
        self.response = response
        self.status_code = response.status_code
        self.result = result
        self.errors = errors

    def get_link(self):
        return self.result.get("link").get("href")

    def follow_link(self):
        return self.http.get(self.get_link())


class HTTP(object):
    def __init__(self, cfg=None):
        self.cfg = cfg
        self.auth = None
        self.base_url = self.cfg.get_endpoint()
        self.session = Session()
        self.session.headers.update(make_headers(
            version=self.cfg.get_version(),
            content_type=self.cfg.get_content_type()))

    def set_auth(self, auth):
        self.auth = auth
        self.session.headers.update(make_auth_header(auth.get_token()))

    def request(self, method, path, **kwargs):
        url = self.base_url + path
        #req = Request(*([method.upper(), url] + list(args)), **kwargs)
        log.debug("kwargs: {}".format(kwargs))
        log.debug("Making request with headers {}...".format(self.session.headers))
        http_func = getattr(self.session, method.lower())
        raw_resp = http_func(url, **kwargs)
        #raw_resp = self.session.send(req.prepare())
        errors = []
        if raw_resp:
            resp = raw_resp.json()
            errors.extend(resp.get("errors") or [])
        else:
            resp = None
        if raw_resp.status_code == 404:
            msg = "Resource not found."
            log.error(msg)
            errors.append(msg)
        # XXX we'll need to change the following to parse the results based on
        # content type, but right now the server is returning the fairly useless
        # application/octet-stream type, even for JSON
        return Response(self, raw_resp, resp.get("result"), errors)

    def post(self, path, **kwargs):
        return self.request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self.request('PUT', path, **kwargs)

    def get(self, path, **kwargs):
        return self.request('GET', path, **kwargs)

    def delete(self, path,**kwargs):
        return self.request('DELETE', path, **kwargs)
