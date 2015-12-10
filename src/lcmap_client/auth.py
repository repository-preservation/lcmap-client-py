import requests

import lcmap_client


context = "/auth"


class Auth(dict):
    def __init__(self, cfg=None, http=None, username="", password="", data={}):
        super(Auth, self).__init__(data)
        self.cfg = cfg
        self.http = http
        self.login(username, password)
        self.refresh_token = self.login

    def login(self, username="", password=""):
        if not username:
            username = self.cfg.get_username()
        if not password:
            password = self.cfg.get_password()
        user_data = self.http.post(
            context + "/login",
            data={"username": username, "password": password})
        self.update(user_data)
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
