import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.polygon import Polygon
from zentangler.point import Point

class TestPolygon(unittest.TestCase):
    def test_intersection_indexes(self):
        polygon = Polygon([Point(0.1, 0.1), Point(0.9, 0.1), Point(0.9, 0.9), Point(0.1, 0.9)])

        #test horizontal line running through square
        p1 = Point(0, 0.5)
        p2 = Point(1, 0.5)
        intersection_indexes = polygon.get_intersection_indexes(p1, p2)
        self.assertEqual(len(intersection_indexes), 2, "found two intersection indexes")
        self.assertEqual(intersection_indexes[0], 1, "first intersection is index 1")
        self.assertEqual(intersection_indexes[1], 3, "first intersection is index 3")

        #test vertical line running through square
        p1 = Point(0.5, 0)
        p2 = Point(0.5, 1)
        intersection_indexes = polygon.get_intersection_indexes(p1, p2)
        self.assertEqual(len(intersection_indexes), 2, "found two intersection indexes")
        self.assertEqual(intersection_indexes[0], 0, "first intersection is index 0")
        self.assertEqual(intersection_indexes[1], 2, "first intersection is index 2")

if __name__ == '__main__':
    unittest.main()