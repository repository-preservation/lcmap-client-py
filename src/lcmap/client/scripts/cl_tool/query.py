import json
import logging

from DateTime import DateTime

import click

import pandas as pd

from lcmap.client import serializer, util
from lcmap.client.client import Client
from lcmap.client.scripts.cl_tool.command import lcmap


log = logging.getLogger(__name__)

spectra_names = util.get_spectra()
spectra_choices = click.Choice(spectra_names)
format_options = ["plain-text", "json"]
format_choices = click.Choice(format_options)


def parse_to_text(results):
    str_results = []
    nil_value = "--"
    field_sep = " "
    record_sep = "\n"
    for (timestamp, data) in results:
        julian = str(DateTime(timestamp).JulianDay())
        str_data = field_sep.join([str(x) for x in data])
        if nil_value not in str_data:
            str_results.append(julian + field_sep + str_data)
    return record_sep.join(str_results)


def parse_to_json(results):
    return json.dumps(combined, indent=4, cls=serializer.NumpyEncoder)


@lcmap.group()
@click.pass_obj
def query(config):
    "Run data queries against the LCMAP Data Warehouse."


# XXX probaly want to move this into the client-proper, and just import it here
def rod_query(spectra, x, y, t1, t2, mask, shape, unscale, format):
    client = Client()
    result = []

    if not spectra:
        spectra = spectra_names

    for s in spectra:
        for b in util.get_spectra(s):
            (spec, rod) = client.data.surface_reflectance.rod(
                b, x, y, t1, t2, mask, shape, unscale)
            for r in rod:
                r['spectrum'] = s
            result.extend(rod)

    # Transform a list of individual band-value maps into
    # band interleaved values.
    df = pd.DataFrame(result)
    pdf = df.pivot(index='source', columns='spectrum')
    adf = pdf['acquired'].iloc[:, 0]
    vdf = pdf['value'].loc[:, spectra]
    return list(zip(adf.values, vdf.values))


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
@click.option('--format', default="plain-text", type=format_choices)
@click.option('--stdout', is_flag=True, default=True)
def rod(config, spectra, x, y, t1, t2, mask, shape, unscale, format, stdout):
    results = rod_query(spectra, x, y, t1, t2, mask, shape, unscale, format)
    if stdout:
        print(results)
    else:
        return results
