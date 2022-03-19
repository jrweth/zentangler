import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from test_shape import SQUARE_SHAPE
from test_polygon import HOLED_POLYGON
from zentangler.shape import Shape
from zentangler.operator.split_operator import SplitOperator
from zentangler.svg import SVG
from zentangler.operator.operator_parameter import OperatorParameterValue

class TestSplitOperator(unittest.TestCase):
    def test_square_simple(self):
        shape: Shape = SQUARE_SHAPE.clone()
        param_values = [
            OperatorParameterValue("width", 0.1)
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])
        self.assertEqual(len(newShapes), 9, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-simple.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

    def test_square_holes(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.075)
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])
        self.assertEqual(len(newShapes), 12, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-holed.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

if __name__ == '__main__':
    unittest.main()