import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.multi_tangle import MultiTangle
from zentangler.shape import Shape
from test_polygon import SQUARE_POLYGON
from shapely.geometry import Polygon, MultiPolygon

square_shape_list = [Shape(geometry=SQUARE_POLYGON)]
triangle_shape_list = [Shape(geometry=MultiPolygon([Polygon([(0.2, 0), (0.8, 0), (0.5, 1)])]))]
rectangle_shape_list = [Shape(geometry=MultiPolygon([Polygon([(0, 0.4), (1, 0.4), (1, 0.6), (0, 0.6)])]))]

class TestSVG(unittest.TestCase):
    def testMultiTangleRandom(self):

        multi_tangle = MultiTangle()
        multi_tangle.init_from_shape_lists_random_grammar([
            square_shape_list,
            triangle_shape_list,
            rectangle_shape_list
        ])
        multi_tangle.create_all()

        svg_filename = SCRIPT_DIR + '/results/test-multitangle-random.svg'
        multi_tangle.create_combined_svg(svg_filename)

    def testMultiTangleCycle(self):

        multi_tangle = MultiTangle()
        multi_tangle.init_from_shape_lists_cycle_grammars([
            square_shape_list,
            triangle_shape_list,
            rectangle_shape_list
        ])
        multi_tangle.create_all()

        svg_filename = SCRIPT_DIR + '/results/test-multitangle-cycle.svg'
        multi_tangle.create_combined_svg(svg_filename)

    def testMultiTangleMoveToBack(self):
        multi_tangle = MultiTangle()
        multi_tangle.init_from_shape_lists_random_grammar([
            square_shape_list,
            triangle_shape_list,
            rectangle_shape_list
        ])
        multi_tangle.create_all()
        multi_tangle.move_to_back(2)

        svg_filename = SCRIPT_DIR + '/results/test-multitangle-move-to-back.svg'
        multi_tangle.create_combined_svg(svg_filename)

    def testMultiTangleMoveToFront(self):
        multi_tangle = MultiTangle()
        multi_tangle.init_from_shape_lists_random_grammar([
            square_shape_list,
            triangle_shape_list,
            rectangle_shape_list
        ])
        multi_tangle.create_all()
        multi_tangle.move_to_front(0)

        svg_filename = SCRIPT_DIR + '/results/test-multitangle-move-to-front.svg'
        multi_tangle.create_combined_svg(svg_filename)

if __name__ == '__main__':
    unittest.main()