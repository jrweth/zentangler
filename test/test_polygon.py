import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
from shapely.geometry import LineString

# a simple square polygon
SQUARE_POLYGON: MultiPolygon = MultiPolygon([
    [[(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], []]
])

HOLE_POLYGON: MultiPolygon = MultiPolygon([
    [[(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], [
        [(0.35, 0.35), (0.65, 0.35), (0.65, 0.65), (0.35, 0.65)]
    ]]
])

#a polygon with some holes
HOLED_POLYGON: MultiPolygon = MultiPolygon([
    [[(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], [
        [(0.35, 0.35), (0.65, 0.35), (0.65, 0.65), (0.35, 0.65)],
        [(0.2, 0.2), (0.3, 0.2), (0.3, 0.3), (0.2, 0.3)]
    ]]
])


class TestPolygon(unittest.TestCase):

    def test_simple_intersection(self):
        geom = SQUARE_POLYGON
        line = LineString([[0.5, 0] , [0.5, 1]]);
        intersections = geom.intersection(line)

        self.assertEqual(len(intersections.coords), 2, "found two intersection indexes")
        self.assertEqual(intersections.coords[0][0], 0.5, "first intersection is at x=0.5")
        self.assertEqual(intersections.coords[0][1], 0.1, "first intersection is at y=0.1")
        self.assertEqual(intersections.coords[1][0], 0.5, "second intersection is at x=0.5")
        self.assertEqual(intersections.coords[1][1], 0.9, "second intersection is at y=0.9")

        #test vertical line running through square
        line = LineString([[0, 0.5], [1, 0.5]]);
        intersections = geom.intersection(line)

        self.assertEqual(len(intersections.coords), 2, "found two intersection indexes")
        self.assertEqual(intersections.coords[0][0], 0.1, "first intersection is at x=0.1")
        self.assertEqual(intersections.coords[0][1], 0.5, "first intersection is at y=0.5")
        self.assertEqual(intersections.coords[1][0], 0.9, "second intersection is at x=0.9")
        self.assertEqual(intersections.coords[1][1], 0.5, "second intersection is at y=0.5")


    def test_holed_intersection(self):
        polygon = HOLED_POLYGON

        line = Polygon([[0.5, 0], [0.5, 1], [0.6, 1], [0.6, 0]])
        intersections = polygon.intersection(line)


if __name__ == '__main__':
    unittest.main()