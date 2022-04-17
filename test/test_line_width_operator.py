import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.operators.line_width_operator import LineWidthOperator
from zentangler.svg import SVG
from zentangler.operators.operator_parameter import OperatorParameterValue



class TestLineWidthOperator(unittest.TestCase):

    def test_line_width(self):
        """
        test making line width greater
        """
        param_values = [
            OperatorParameterValue("width_or_multiplier", "width"),
            OperatorParameterValue("line_width", 0.03)
        ]
        operator = LineWidthOperator(param_values)

        shapes = operator.get_thumbnail_shapes_grid(0.25)

        new_shapes = operator.execute(shapes, ["big_line"])

        svg = SVG(SCRIPT_DIR + '/results/test-linewidth-operator-width.svg')
        for shape in new_shapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(new_shapes[0].stroke_width, 0.03, "stroke width has been updated")
        self.assertEqual(new_shapes[0].tag, "big_line", "new tag matches 'big line'")

    def test_line_mutliplier(self):
        """
        test multiplying the line width
        """
        param_values = [
            OperatorParameterValue("width_or_multiplier", "current_width_multiplier"),
            OperatorParameterValue("current_width_multiplier", 0.25)
        ]
        operator = LineWidthOperator(param_values)

        shapes = operator.get_thumbnail_shapes_grid(0.25)

        new_shapes = operator.execute(shapes, ["multiplied_line"])

        svg = SVG(SCRIPT_DIR + '/results/test-linewidth-operator-multiplier.svg')
        for shape in new_shapes:
            svg.add_shape(shape)
        svg.save_svg()

        self.assertEqual(new_shapes[0].stroke_width, 0.0025, "stroke width has been updated")
        self.assertEqual(new_shapes[0].tag, "multiplied_line", "new tag matches 'big line'")


    def test_linewidth_thumbnail(self):
        param_values = [
            OperatorParameterValue("width", 0.05)
        ]
        operator = LineWidthOperator(param_values)
        png_filename = SCRIPT_DIR + '/results/test-linewidth-operator-thumbnail.png'
        operator.create_thumbnail(png_filename)


if __name__ == '__main__':
    unittest.main()