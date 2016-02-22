import click

from lcmap.client.scripts.cl_tool.lcmap import lcmap


@lcmap.group()
@click.pass_obj
def model(config):
    "TBD: Execute science models in the LCMAP Science Execution Environment."
