import sys
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
