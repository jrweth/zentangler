import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.svg import SVG
from zentangler.shape import Shape
from test_polygon import HOLED_POLYGON

class TestSVG(unittest.TestCase):
    def testSVG(self):
        svg = SVG(SCRIPT_DIR + '/results/test-svg.svg')
        shape = Shape(geometry=HOLED_POLYGON)
        svg.add_shape(shape)
        svg.save_svg()

    def testSVGtoPNG(self):
        svg = SVG(SCRIPT_DIR + '/results/test-svg.svg')
        shape = Shape(geometry=HOLED_POLYGON)
        svg.add_shape(shape)
        svg.save_png('results/test-svg-png.png')

if __name__ == '__main__':
    unittest.main()