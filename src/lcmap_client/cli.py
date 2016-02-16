import click
import json
import logging
import numpy as np
import pandas as pd

from lcmap_client import Client


log = logging.getLogger(__name__)


spectra_to_bands = {
    'blue': [
        'LANDSAT_8/OLI_TIRS/sr_band2',
        'LANDSAT_7/ETM/sr_band1',
        'LANDSAT_5/TM/sr_band1'
    ],
    'green': [
        'LANDSAT_8/OLI_TIRS/sr_band3',
        'LANDSAT_7/ETM/sr_band2',
        'LANDSAT_5/TM/sr_band2'
    ],
    'red': [
        'LANDSAT_8/OLI_TIRS/sr_band4',
        'LANDSAT_7/ETM/sr_band3',
        'LANDSAT_5/TM/sr_band3'
    ],
    'ir': [
        'LANDSAT_8/OLI_TIRS/sr_band5',
        'LANDSAT_7/ETM/sr_band4',
        'LANDSAT_5/TM/sr_band4'
    ],
    'swir-1': [
        'LANDSAT_8/OLI_TIRS/sr_band6',
        'LANDSAT_7/ETM/sr_band5',
        'LANDSAT_5/TM/sr_band5'
    ],
    'swir-2': [
        'LANDSAT_8/OLI_TIRS/sr_band7',
        'LANDSAT_7/ETM/sr_band7',
        'LANDSAT_5/TM/sr_band7'
    ],
    'tirs-1': [
        'LANDSAT_8/OLI_TIRS/toa_band10',
        'LANDSAT_7/ETM/toa_band6',
        'LANDSAT_5/TM/toa_band6'
    ],
    'cf': [
        'LANDSAT_8/OLI_TIRS/cfmask',
        'LANDSAT_7/ETM/cfmask',
        'LANDSAT_5/TM/cfmask'
    ]
}


spectra_choices = click.Choice(
    ['blue', 'green', 'red', 'ir', 'swir-1', 'swir-2', 'tirs-1', 'cf'])


@click.group()
def cli():
    pass


@click.command()
@click.option('--spectra', '-s', multiple=True, type=spectra_choices)
@click.option('--x', '-x', type=int)
@click.option('--y', '-y', type=int)
@click.option('--t1')
@click.option('--t2')
def rod(spectra, x, y, t1, t2):
    client = Client()

    if not spectra:
        spectra = spectra_to_bands.keys()
        print(spectra)

    result = []
    for s in spectra:
        for b in spectra_to_bands.get(s):
            spec, rod = client.data.surface_reflectance.rod(b, x, y, t1, t2)
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
    print(json.dumps(combined, indent=4, cls=NumpyEncoder))


cli.add_command(rod)


# This only support encoding of types that are retrieved
# from the LCMAP REST API; it is not comprehensive.
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.int8):
            return int(obj)
        else:
            return obj.__repr__()
