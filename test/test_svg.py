import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.svg import SVG
from shapely.geometry import Polygon
from zentangler.shape import Shape
from test_polygon import HOLED_POLYGON

class TestSVG(unittest.TestCase):
    def testSVG(self):
        svg = SVG(SCRIPT_DIR + '/results/test-svg.svg')
        shape = Shape(geometry=HOLED_POLYGON)
        svg.add_shape(shape)
        svg.save_svg()

if __name__ == '__main__':
    unittest.main()