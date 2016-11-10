import click

from lcmap.client.scripts.cl_tool.command import lcmap


@lcmap.group()
@click.pass_obj
def job(config):
    "TBD: Check on the status of LCMAP jobs."
