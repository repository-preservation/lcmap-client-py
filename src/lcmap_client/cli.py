import click
import json

from lcmap_client import Client

spectra_to_bands = {
  'red':[
    'LANDSAT_8/OLI_TIRS/sr_band4'
  ],
  'green':[
    'LANDSAT_8/OLI_TIRS/sr_band3'
  ],
  'blue':[
    'LANDSAT_8/OLI_TIRS/sr_band2'
  ]
}


@click.command()
@click.option('--spectra', '-s', multiple=True)
@click.option('--x', '-x', type=int)
@click.option('--y', '-y', type=int)
@click.option('--t1')
@click.option('--t2')
def get_rod(spectra, x, y, t1, t2):
  client = Client()
  result = []
  for s in spectra:
    for b in spectra_to_bands.get(s):
      spec, rod = client.data.surface_reflectance.rod(b, x, y, t1, t2)
      result.append({ spec['ubid']: rod })
  print(json.dumps(result, indent=4))
  return result