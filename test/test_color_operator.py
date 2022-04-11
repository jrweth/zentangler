import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.svg import SVG
from zentangler.shape import Shape
from test_shape import SQUARE_SHAPE
from zentangler.operators.split_operator import SplitOperator
from zentangler.operators.color_operator import ColorOperator
from zentangler.operators.operator_parameter import OperatorParameterValue

class TestColorOperator(unittest.TestCase):
    def test_assign_single(self):
        """
        test splitting the simple square and then assigning colors
        """
        shape: Shape = SQUARE_SHAPE.clone()
        param_values = [
            OperatorParameterValue("line_colors", [(1, 0, 0)]),
            OperatorParameterValue("line_color_assignment", "single color"),
            OperatorParameterValue("fill_colors", [(0, 1, 0)]),
            OperatorParameterValue("fill_color_assignment", "single color"),
        ]
        color_operator = ColorOperator(param_values)

        new_shapes: list[Shape] = color_operator.execute([shape], ['colored'])

        svg = SVG(SCRIPT_DIR + '/results/test-color-operator-single.svg')
        for shape in new_shapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(new_shapes[0].stroke_color[0], 1, "red stroke value matches")
        self.assertEqual(new_shapes[0].fill_color[1], 1, "green fill value matches")
        self.assertEqual(new_shapes[0].tag, 'colored', "new tag matches")


    def test_assign_cycle(self):
        """
        test splitting the simple square and then assigning cycle colors
        """
        shape: Shape = SQUARE_SHAPE.clone()
        split_params = [
            OperatorParameterValue("width", 0.2),
            OperatorParameterValue("cross_split", True),
        ]
        split_operator = SplitOperator(split_params)
        split_shapes = split_operator.execute([shape], ["split"])

        param_values = [
            OperatorParameterValue("line_colors", [(1, 0, 0), (0, 1, 0), (0, 0, 1)]),
            OperatorParameterValue("line_color_assignment", "cycle colors"),
            OperatorParameterValue("fill_colors", [(0, 1, 0), (0, 0, 1), (1, 0, 0)]),
            OperatorParameterValue("fill_color_assignment", "cycle colors"),
        ]
        color_operator = ColorOperator(param_values)

        new_shapes: list[Shape] = color_operator.execute(split_shapes, ['colored'])

        svg = SVG(SCRIPT_DIR + '/results/test-color-operator-cycle.svg')
        for shape in new_shapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(new_shapes[0].stroke_color[0], 1, "red stroke value matches")
        self.assertEqual(new_shapes[0].fill_color[1], 1, "green fill value matches")
        self.assertEqual(new_shapes[1].stroke_color[1], 1, "red stroke value matches")
        self.assertEqual(new_shapes[1].fill_color[2], 1, "green fill value matches")
        self.assertEqual(new_shapes[0].tag, 'colored', "new tag matches")

    def test_assign_random(self):
        """
        test splitting the simple square and then assigning cycle colors
        """
        shape: Shape = SQUARE_SHAPE.clone()
        split_params = [
            OperatorParameterValue("width", 0.2),
            OperatorParameterValue("cross_split", True),
        ]
        split_operator = SplitOperator(split_params)
        split_shapes = split_operator.execute([shape], ["split"])

        param_values = [
            OperatorParameterValue("line_color_assignment", "random"),
            OperatorParameterValue("fill_color_assignment", "random"),
            OperatorParameterValue("random_seed", 4),
        ]
        color_operator = ColorOperator(param_values)

        new_shapes: list[Shape] = color_operator.execute(split_shapes, ['colored'])

        svg = SVG(SCRIPT_DIR + '/results/test-color-operator-random.svg')
        for shape in new_shapes:
            svg.add_shape(shape)
        svg.save_svg()

        # self.assertEqual(new_shapes[0].stroke_color[0], 1, "red stroke value matches")
        # self.assertEqual(new_shapes[0].fill_color[1], 1, "green fill value matches")
        # self.assertEqual(new_shapes[1].stroke_color[1], 1, "red stroke value matches")
        # self.assertEqual(new_shapes[1].fill_color[2], 1, "green fill value matches")
        self.assertEqual(new_shapes[0].tag, 'colored', "new tag matches")

if __name__ == '__main__':
    unittest.main()