import click

from lcmap_client.scripts.cl_tool.lcmap import lcmap


@lcmap.group()
@click.pass_obj
def system(config):
    "TBD: Perform LCMAP system management tasks (requires elevated privledges)."
