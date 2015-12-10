import logging

from os import environ, path

from six.moves.configparser import ConfigParser

from pylru import lrudecorator

from lcmap_client import http, logger

log = logging.getLogger(__name__)
home = path.expanduser("~")
ini_file = path.join(home, ".usgs", "lcmap.ini")


@lrudecorator(1024)
def reader(filename=None):
    if filename is None:
        filename=ini_file
    cfg = ConfigParser()
    log.debug("Reading configuration from {} ...".format(ini_file))
    cfg.read(filename)
    return cfg


def get_env(key):
    return environ.get("LCMAP_" + key.upper())


class Config:
    def __init__(self, filename=None, force_reload=False):
        self.filename = filename
        self.reader = None
        if force_reload:
            self.reload()
        else:
            self.load()

    def load(self):
        self.ini = reader(self.filename)

    def reload(self):
        reader.clear()
        self.load()

    # Configuration accessors
    def get(self, section="LCMAP Client", key=None):
        env = get_env(key)
        if env:
            return env
        return self.ini.get(section, key)

    def get_username(self):
        return self.get(key="username")

    def get_password(self):
        return self.get(key="password")

    def get_version(self):
        return self.get(key="version")

    def get_endpoint(self):
        return self.get(key="endpoint")

    def get_content_type(self):
        return self.get(key="content-type")

    def get_log_level(self):
        return logger.serialize_level(self.get(key="log-level"))

    def get_logging_namespaces(self):
        return self.get(key="logging-namespaces")



