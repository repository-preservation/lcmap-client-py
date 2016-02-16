import click

import logging


log = logging.getLogger(__name__)


@click.group()
@click.option("--log-level", envvar="LCMAP_LOG_LEVEL",
                             default="error",
                             help=("Set the lcmap tool's level of verbosity."
                                   "Valid values are 'debug', 'info', 'warn', "
                                   "'error', and 'fail'."))
@click.pass_context
def lcmap(context, log_level):
    """The lcmap command line tool.

    'lcmap' allows you to easily execute queries against the LCMAP service
    from the command line, facilitating integration with exitsting tools
    and workflows.
    """
