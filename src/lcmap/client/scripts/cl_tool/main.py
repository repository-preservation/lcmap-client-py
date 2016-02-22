"""
The main module for the lcmap command-line tool serves two important functions:

1. It offers the `main` entry point for setuptools, and
2. It imports all of the subcommands necessary in order for the tool's command
   functions to be properly decorated before getting called in `main()`.
"""
# flake8: noqa
from lcmap.client.scripts.cl_tool import (job, lcmap, model, monitor, query,
                                          system)

def main():
    lcmap.lcmap()
