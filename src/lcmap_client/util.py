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


def get_spectra(key=None):
    if not key:
        data = spectra_to_bands.keys()
    else:
        data = spectra_to_bands[key]
    return data
