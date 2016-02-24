import click

from lcmap.client.scripts.cl_tool.command import lcmap


@lcmap.group()
@click.pass_obj
def model(config):
    "TBD: Execute science models in the LCMAP Science Execution Environment."
