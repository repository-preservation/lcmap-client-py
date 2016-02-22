import click

from lcmap.client.scripts.cl_tool.lcmap import lcmap


@lcmap.group()
@click.pass_obj
def system(config):
    "TBD: Perform LCMAP system management tasks (requires elevated privledges)."
