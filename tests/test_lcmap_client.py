import unittest

from lcmap_client import Client
from lcmap_client import util

if __name__ == '__main__':
    unittest.main()

class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.params = {'band': 'LANDSAT_8/OLI_TIRS/sr_band2',
                       'time': '2013-01-01/2014-01-01',
                       'point': '-1850865,2956785'}
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

    def test_rods(self):
        pass

    def test_upper_left_proj_point_to_tile_point(self):
        t = util.image_transform(self.tile, self.spec)
        x = -1850865
        y =  2956785
        point = util.proj_point_to_tile_point(x, y, t)
        self.assertEqual(point, (0,0))

    def test_upper_right_proj_point_to_tile_point(self):
        t = util.image_transform(self.tile, self.spec)
        x = -1850865 + (30*256)
        y =  2956785
        point = util.proj_point_to_tile_point(x, y, t)
        self.assertEqual(point, (256,0))

    def test_lower_left_proj_point_to_tile_point(self):
        t = util.image_transform(self.tile, self.spec)
        x = -1850865
        y =  2956785 + ((-30)*256)
        point = util.proj_point_to_tile_point(x, y, t)
        self.assertEqual(point, (0,256))

    def test_lower_right_proj_point_to_tile_point(self):
        t = util.image_transform(self.tile, self.spec)
        x = -1850865 + (30*256)
        y =  2956785 + ((-30)*256)
        point = util.proj_point_to_tile_point(x, y, t)
        self.assertEqual(point, (256,256))

    def test_proj_point_offset_from_pixel_grid(self):
        t = util.image_transform(self.tile, self.spec)
        x = -1850865+2
        y =  2956785-2
        point = util.proj_point_to_tile_point(x, y, t)
        self.assertEqual(point, (0,0))  