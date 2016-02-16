import unittest

from lcmap_client import Client
from lcmap_client import geom


if __name__ == '__main__':
    unittest.main()


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.params = {
            'band': 'LANDSAT_8/OLI_TIRS/sr_band2',
            'x':    -1850865,
            'y':     2956785,
            't1':   '2013-01-01',
            't2':   '2015-01-01'
        }
        self.spec, self.tiles = self.client.data.surface_reflectance.tiles(**self.params)
        self.tile = self.tiles[0]

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsNotNone(self.client)

    def test_tile_point(self):
        self.assertEqual(self.tile.x, -1850865)
        self.assertEqual(self.tile.y,  2956785)

    def test_tile_acquired(self):
        self.assertEqual(self.tile.acquired, '2013-08-04T00:00:00Z')

    def test_tile_ubid(self):
        self.assertEqual(self.tile.ubid, 'LANDSAT_8/OLI_TIRS/sr_band2')

    def test_tile_shape(self):
        self.assertEqual(self.tile.data.shape, (256,256))

    def test_tile_data(self):
        px,py = -1850865, 2956785
        tx,ty = 0, 0
        self.assertEqual(self.tile[px,py], self.tile.data[tx,ty])
        px,py = -1850865+30, 2956785-30
        tx,ty = 1, 1
        self.assertEqual(self.tile[px,py], self.tile.data[tx,ty])
        px,py = -1850865+(30*128), 2956785-(30*128)
        tx,ty = 128, 128
        self.assertEqual(self.tile[px,py], self.tile.data[tx,ty])
