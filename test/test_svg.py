import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.svg import SVG
from zentangler.polygon import Polygon
from zentangler.shape import Shape
from zentangler.point import Point

class TestSVG(unittest.TestCase):
    def testSVG(self):
        svg = SVG(SCRIPT_DIR + '/results/test-svg.svg')
        outer_polygon = Polygon([Point(0.1, 0.1), Point(0.9, 0.1), Point(0.9, 0.9), Point(0.1, 0.9)])
        inner_polygons = [
            Polygon([Point(0.4, 0.4), Point(0.6, 0.4), Point(0.6, 0.6), Point(0.4, 0.6)]),
            Polygon([Point(0.2, 0.2), Point(0.3, 0.2), Point(0.3, 0.3), Point(0.2, 0.3)])
        ]
        shape = Shape(outer_polygon=outer_polygon, inner_polygons=inner_polygons)
        svg.add_shape(shape)
        svg.save_svg()

if __name__ == '__main__':
    unittest.main()