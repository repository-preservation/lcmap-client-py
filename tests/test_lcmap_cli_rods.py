import pickle
import unittest

from lcmap.client import Client, geom
from lcmap.client.scripts.cl_tool import query


class RodResultTestCase(unittest.TestCase):

    def setUp(self):
        with open("tests/data/cli-rod-results.pkl", "rb") as data:
            self.results = pickle.load(data)

    def test_parse_as_text(self):
        with open("tests/data/cli-rod-results.txt", "r") as expected:
            parsed = query.parse_to_text(self.results)
            self.assertEqual(parsed, expected.read().strip())


class RodResult3YearsTestCase(unittest.TestCase):

    def setUp(self):
        with open("tests/data/cli-rod-3yrs-results.pkl", "rb") as data:
            self.results = pickle.load(data)

    def test_parse_as_text(self):
        with open("tests/data/cli-rod-3yrs-results.txt", "r") as expected:
            parsed = query.parse_to_text(self.results)
            self.assertEqual(parsed, expected.read().strip())


if __name__ == '__main__':
    unittest.main()
