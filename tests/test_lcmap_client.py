import unittest

from lcmap.client import Client


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        # corner of tile, api currently reporting
        # floor, 'should' be ceil
        self.tx, self.ty = -1850880, 2952960
        # random geo coords
        self.px, self.py = -1850865, 2956785
        self.params = {
            'band': 'LANDSAT_8/OLI_TIRS/sr_band2',
            'x': self.px,
            'y': self.py,
            't1':   '2013-01-01',
            't2':   '2015-01-01'
        }
        self.spec, self.tiles = self.client.data.tiles(**self.params)
        self.tile = self.tiles[0]

    def test_init(self):
        self.assertIsNotNone(self.client)

    def test_tile_point(self):
        self.assertEqual(self.tile.x, self.tx)
        self.assertEqual(self.tile.y, self.ty)

    def test_tile_acquired(self):
        self.assertEqual(self.tile.acquired, '2013-04-14T05:00:00Z')

    def test_tile_ubid(self):
        self.assertEqual(self.tile.ubid, 'LANDSAT_8/OLI_TIRS/sr_band2')

    def test_tile_shape(self):
        self.assertEqual(self.tile.data.shape, (128, 128))

    def test_tile_data(self):
        x, y = self.tx, self.ty
        tx, ty = 0, 0
        self.assertEqual(self.tile[x, y], self.tile.data[tx, ty])
        x, y = self.tx+30, self.ty-30
        tx, ty = 1, 1
        self.assertEqual(self.tile[x, y], self.tile.data[tx, ty])
        x, y = self.tx+(30*127), self.ty-(30*127)
        tx, ty = 127, 127
        self.assertEqual(self.tile[x, y], self.tile.data[tx, ty])


if __name__ == '__main__':
    unittest.main()
