import click

from lcmap.client.scripts.cl_tool.command import lcmap


@lcmap.group()
@click.pass_obj
def monitor(config):
    """TBD: Commands for subscriptions and notifications in the LCMAP land
    monitoring system."""
