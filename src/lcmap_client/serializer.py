import json


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for NumPy data types.

    This only support encoding of types that are retrieved
    from the LCMAP REST API; it is not comprehensive.
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.int8):
            return int(obj)
        else:
            return repr(obj)
