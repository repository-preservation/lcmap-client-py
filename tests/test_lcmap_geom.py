import unittest

from lcmap_client import geom
from lcmap_client.data import surface_reflectance


if __name__ == '__main__':
    unittest.main()


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        params = {
            'band': 'LANDSAT_8/OLI_TIRS/sr_band2',
            'x':    -1850865,
            'y':     2956785,
            't1':   '2013-01-01',
            't2':   '2015-01-01'
        }
        # XXX instead of None, we need to pass a fake object that has a
        #     callable "get" attribute on it (e.g., lambda) which returns
        #     a FakeResponse - an object with a "result" attr that is a
        #     dictionary and has a "spec" key and a "tiles" key that is a list
        #     of fake payload data (e.g., a list containing one tile).
        sr = surface_reflectance.SurfaceReflectance(None)
        self.spec, self.tiles = sr.tiles(**params)
        self.tile = self.tiles[0]
        self.xform_matrix = geom.get_transform_matrix(self.tile, self.spec)


class PublicFunctionsTestCase(BaseTestCase):

    def test_transform_coord_map_to_image_upper_left(self):
        coord = (-1850865, 2956785)
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0,0))

    def test_transform_coord_map_to_image_upper_right(self):
        coord = (-1850865+(30*255), 2956785)
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (255,0))

    def test_transform_coord_map_to_image_lower_left(self):
        coord = (-1850865, 2956785 + ((-30)*(256-1)))
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0,255))

    def test_transform_coord_map_to_image_lower_right(self):
        coord = (-1850865+(30*255), 2956785+((-30)*255))
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (255,255))

    def test_transform_coord_map_to_image_offset(self):
        coord  = (-1850865+2, 2956785-2)
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0,0))

    def test_rod(self):
        # XXX what's up with this test? it's just asserting that the rod is an
        #     empty list -- if it's not implemented, let's dsiable the test
        (x, y) = (-1850865, 2956785)
        rod = [(t.acquired, t[x,y]) for t in self.tiles]
        self.assertEqual([], rod)


class PrivateFunctionsTestCase(BaseTestCase):

    def test_upper_left_proj_point_to_tile_point(self):
        (px, py) = (-1850865, 2956785)
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (0,0))

    def test_upper_right_proj_point_to_tile_point(self):
        (px, py) = (-1850865+(30*255), 2956785)
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (255,0))

    def test_lower_left_proj_point_to_tile_point(self):
        (px, py) = (-1850865, 2956785 + ((-30)*(256-1)))
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (0,255))

    def test_lower_right_proj_point_to_tile_point(self):
        (px, py) = (-1850865+(30*255), 2956785+((-30)*255))
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (255,255))

    def test_proj_point_offset_from_pixel_grid(self):
        (px, py)  = (-1850865+2, 2956785-2)
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (0,0))
