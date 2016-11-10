"""
The authentication module holds the Auth class which is is not only responsible
for the action of logging in, but also providing accessor method to the data
obtained upon a successful login.
"""
import logging

from lcmap.client.api import routes


log = logging.getLogger(__name__)

context = routes.auth_context
login_context = context + "/login"
user_context = context + "/me"


class Auth(dict):
    def __init__(self, cfg=None, http=None, username="", password="", data={}):
        super(Auth, self).__init__(data)
        self.cfg = cfg
        self.http = http
        self.login(username, password)
        self.refresh_token = self.login

    def login(self, username="", password=""):
        log.debug("Logging in ...")
        log.debug(login_context)
        if not username:
            username = self.cfg.get_username()
        if not password:
            password = self.cfg.get_password()
        result = self.http.post(
            login_context,
            data={"username": username, "password": password})
        if result.errors:
            log.error("Login unsuccessful: {}".format(result.errors))
        self.update(result.result)
        self.http.set_auth(self)
        return self

    def get_token(self):
        return self.get("token")

    def get_userid(self):
        return self.get("user-id")

    def get_username(self):
        return self.get("username")

    def get_roles(self):
        return self.get("roles")

    def get_email(self):
        return self.get("email")
