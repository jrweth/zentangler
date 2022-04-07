import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from test_shape import SQUARE_SHAPE
from test_polygon import HOLED_POLYGON
from zentangler.shape import Shape
from zentangler.operators.split_operator import SplitOperator
from zentangler.svg import SVG
from zentangler.operators.operator_parameter import OperatorParameterValue

class TestSplitOperator(unittest.TestCase):
    def test_square_simple(self):
        """
        test splitting the simple square
        """
        shape: Shape = SQUARE_SHAPE.clone()
        param_values = [
            OperatorParameterValue("width", 0.1)
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-simple.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(len(newShapes), 9, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")

    def test_square_holes(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.075),
            OperatorParameterValue("angle", -30)
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-holed.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(len(newShapes), 16, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")


    def test_cross(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.2),
            OperatorParameterValue("angle", 30),
            OperatorParameterValue("cross_split", True)
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-cross.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(len(newShapes), 27, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")

    def test_jagged(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.1),
            OperatorParameterValue("line_style", "JAGGED"),
            OperatorParameterValue("line_style_scale_x", .3),
            OperatorParameterValue("line_style_scale_y", .5),
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-jagged.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(len(newShapes), 12, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")

    def test_stepped(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.1),
            OperatorParameterValue("line_style", "STEPPED"),
            OperatorParameterValue("line_style_scale_x", .1),
            OperatorParameterValue("line_style_scale_y", .1),
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-stepped.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(len(newShapes), 9, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")


    def test_curved(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.1),
            OperatorParameterValue("line_style", "CURVED"),
            OperatorParameterValue("line_style_scale_x", .3),
            OperatorParameterValue("line_style_scale_y", .1),
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-curved.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(len(newShapes), 11, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")

    def test_half_circle(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.1),
            OperatorParameterValue("line_style", "HALF_CIRCLE"),
            OperatorParameterValue("line_style_scale_x", .5),
            OperatorParameterValue("line_style_scale_y", .75),
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-half-circle.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(len(newShapes), 12, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")



    def test_noise(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.1),
            OperatorParameterValue("line_style", "NOISE"),
            OperatorParameterValue("line_style_scale_x", 0.4),
            OperatorParameterValue("line_style_scale_y", 0.4),
            OperatorParameterValue("random_seed", 2)
        ]
        splitOperator = SplitOperator(param_values)

        newShapes: list[Shape] = splitOperator.execute([shape], ['split'])

        svg = SVG(SCRIPT_DIR + '/results/test-split-operator-noise.svg')
        for shape in newShapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(len(newShapes), 10, "number of split shapes equal")
        self.assertEqual(newShapes[0].tag, "split", "new tag name should equal split")

if __name__ == '__main__':
    unittest.main()