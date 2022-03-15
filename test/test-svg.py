import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.svg import SVG
from zentangler.polygon import Polygon
from zentangler.shape import Shape

class TestSVG(unittest.TestCase):
    def testSVG(self):
        svg = SVG(SCRIPT_DIR + '/results/test-svg.svg')
        outer_polygon = Polygon([[0.1, 0.1], [0.9, 0.1], [0.9, 0.9], [0.1, 0.9]])
        inner_polygons = [
            Polygon([[0.4, 0.4], [0.6, 0.4], [0.6, 0.6], [0.4, 0.6]]),
            Polygon([[0.2, 0.2], [0.3, 0.2], [0.3, 0.3], [0.2, 0.3]])
        ]
        shape = Shape(outer_polygon, inner_polygons)
        svg.add_shape(shape)
        svg.save_svg()

if __name__ == '__main__':
    unittest.main()