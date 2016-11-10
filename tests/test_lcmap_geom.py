import unittest
from lcmap.client import Client, geom


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        # corner of tile, api currently reporting
        # floor, 'should' be ceil
        self.tx, self.ty = -1850880, 2952960
        # random geo coords
        self.px, self.py = -1850865, 2956785
        self.coord = self.px, self.py
        self.params = {
            'band': 'LANDSAT_8/OLI_TIRS/sr_band2',
            'x': self.px,
            'y': self.py,
            't1':   '2013-01-01',
            't2':   '2015-01-01'
        }
        self.spec, self.tiles = self.client.data.tiles(**self.params)
        self.tile = self.tiles[0]
        self.xform_matrix = self.tile._point_transformer
        # tiles are 128 x 128 pixels
        self.tile_len = 128
        self.data_shape = [self.tile_len, self.tile_len]
        # tile index starts at 0
        self.tile_ind = self.tile_len - 1
        # pixel resolution 30m
        self.tile_res = 30


class ObjectsTestCase(BaseTestCase):
    "Make sure that all the bits are set up properly."

    def test_spec(self):
        self.assertEqual(self.spec["data_shape"], self.data_shape)

    def test_tiles(self):
        self.assertEqual(len(self.tiles), 38)

    def test_tile(self):
        self.assertEqual(type(self.tile).__name__, "Tile")
        self.assertEqual(self.tile.spec, self.spec)

    def test_xform_matrix(self):
        self.assertEqual(type(self.xform_matrix).__name__, "GeoAffine")
        self.assertEqual(self.xform_matrix[0], self.tx)


class PublicFunctionsTestCase(BaseTestCase):

    def test_transform_coord_map_to_image_upper_left(self):
        point = geom.transform_coord(
                self.coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0, -self.tile_ind))

    def test_transform_coord_map_to_image_upper_right(self):
        coord = self.px+(self.tile_res*self.tile_ind), self.py
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (self.tile_ind, -self.tile_ind))

    def test_transform_coord_map_to_image_lower_left(self):
        coord = self.px, self.py + ((-self.tile_res)*self.tile_ind)
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0, 0))

    def test_transform_coord_map_to_image_lower_right(self):
        coord = self.px+(self.tile_res*self.tile_ind), self.py+((-self.tile_res)*self.tile_ind)
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (self.tile_ind, 0))

    def test_transform_coord_map_to_image_offset(self):
        coord = self.px+2, self.py-2
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0, -self.tile_ind))

    def test_rod(self):
        rod = [(t.acquired, t[self.px, self.py]) for t in self.tiles]
        self.assertEqual([('2013-04-14T05:00:00Z', 0.87080000000000002),
                          ('2013-04-30T05:00:00Z', 0.65439999999999998)],
                         rod[:2])
        self.assertEqual(len(rod), 38)


class PrivateFunctionsTestCase(BaseTestCase):

    def test_upper_left_proj_point_to_tile_point(self):
        point = geom._proj_point_to_tile_point(self.px, self.py, self.xform_matrix)
        self.assertEqual(point, (0, -self.tile_ind))

    def test_upper_right_proj_point_to_tile_point(self):
        px, py = self.px+(self.tile_res*self.tile_ind), self.py
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (self.tile_ind, -self.tile_ind))

    def test_lower_left_proj_point_to_tile_point(self):
        px, py = self.px, self.py + ((-self.tile_res)*self.tile_ind)
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (0, 0))

    def test_lower_right_proj_point_to_tile_point(self):
        px, py = self.px+(self.tile_res*self.tile_ind), self.py+((-self.tile_res)*self.tile_ind)
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (self.tile_ind, 0))

    def test_proj_point_offset_from_pixel_grid(self):
        px, py  = self.px+2, self.py-2
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (0, -self.tile_ind))


if __name__ == '__main__':
    unittest.main()
