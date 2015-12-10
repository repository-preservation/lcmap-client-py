from requests import Request, Session

from lcmap_client import auth, http, logger
from lcmap_client.config import Config


class BaseClient(object):
    def __init__(self, base_context=""):
        self.base_context = base_context
        self.cfg = Config()
        self.base_url = "{}{}".format(
            self.cfg.get_endpoint(), self.base_context)
        logger.configure(self.cfg)
        self.session = Session()
        self.session.headers.update(http.get_base_headers())
        self.user_data = None
        self.login()

    def login(self, username="", password=""):
        if not username:
            username = self.cfg.get_username()
        if not password:
            password = self.cfg.get_password()
        user_data = self.post(
            auth.context + "/login",
            data={"username": username, "password": password})
        self.user_data = auth.UserData(user_data)
        return self.user_data

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
