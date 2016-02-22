import click

from lcmap.client.scripts.cl_tool.lcmap import lcmap


@lcmap.group()
@click.pass_obj
def job(config):
    "TBD: Check on the status of LCMAP jobs."
