import json
import logging

import click

import pandas as pd

from lcmap.client import Client, serializer, util
from lcmap.client.scripts.cl_tool.lcmap import lcmap


log = logging.getLogger(__name__)

spectra_names = util.get_spectra()
spectra_choices = click.Choice(spectra_names)


@lcmap.group()
@click.pass_obj
def query(config):
    "Run data queries against the LCMAP Data Warehouse."


@query.command()
@click.pass_obj
@click.option('--spectra', '-s', multiple=True, type=spectra_choices)
@click.option('--x', '-x', type=int)
@click.option('--y', '-y', type=int)
@click.option('--t1')
@click.option('--t2')
@click.option('--mask/--no-mask', is_flag=True, default=True)
@click.option('--shape/--no-shape', is_flag=True, default=True)
@click.option('--unscale/--scale', is_flag=True, default=True)
def rod(config, spectra, x, y, t1, t2, mask, shape, unscale):
    client = Client()

    if not spectra:
        spectra = ['blue', 'green', 'red','ir','swir-1','swir-2,''tirs-1','cf']

    result = []
    for s in spectra:
        for b in util.get_spectra(s):
            (spec, rod) = client.data.surface_reflectance.rod(b, x, y, t1, t2, mask, shape, unscale)
            for r in rod:
                r['spectrum'] = s
            result.extend(rod)

    # Transform a list of individual band-value maps into
    # band interleaved values.
    df = pd.DataFrame(result)
    pdf = df.pivot(index='source', columns='spectrum')
    adf = pdf['acquired'].iloc[:, 0]
    vdf = pdf['value'].loc[:, spectra]
    combined = list(zip(adf.values, vdf.values))
    fh = open("meow-is-not-a-file-name","w")
    print(json.dumps(combined, indent=4, cls=serializer.NumpyEncoder))