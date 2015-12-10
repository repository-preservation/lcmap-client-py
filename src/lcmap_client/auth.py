import requests

import lcmap_client


context = "/auth"


class UserData(dict):

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
