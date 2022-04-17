import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from test_shape import SQUARE_SHAPE
from test_polygon import HOLED_POLYGON, HOLE_POLYGON
from zentangler.shape import Shape
from zentangler.operators.grouping_operator import RegroupOperator, UngroupOperator, get_sample_group_color
from zentangler.svg import SVG
from zentangler.operators.operator_parameter import OperatorParameterValue



class TestGroupingOperator(unittest.TestCase):

    def test_regroup2(self):
        """
        test splitting the simple square
        """
        param_values = [
            OperatorParameterValue("k", 2)
        ]
        operator = RegroupOperator(param_values)

        shapes = operator.get_thumbnail_shapes_grid(0.25)

        new_shapes = operator.execute(shapes, [])

        self.assertEqual(new_shapes[0].group_id, 0, "first shape is group id 0")
        self.assertEqual(new_shapes[1].group_id, 1, "second shape is group id 1")
        self.assertEqual(new_shapes[2].group_id, 0, "third shape is group id 0")

        svg = SVG(SCRIPT_DIR + '/results/test-regroup-operator-2.svg')
        for shape in new_shapes:
            shape.fill_color = get_sample_group_color(shape.group_id)
            svg.add_shape(shape)
        svg.save_svg()

    def test_regroup3(self):
        """
        test splitting the simple square
        """
        param_values = [
            OperatorParameterValue("k", 3)
        ]
        operator = RegroupOperator(param_values)

        shapes = operator.get_thumbnail_shapes_grid(0.25)

        new_shapes = operator.execute(shapes, [])

        self.assertEqual(new_shapes[0].group_id, 0, "first shape is group id 0")
        self.assertEqual(new_shapes[1].group_id, 1, "second shape is group id 1")
        self.assertEqual(new_shapes[2].group_id, 2, "third shape is group id 2")
        self.assertEqual(new_shapes[3].group_id, 0, "fourth shape is group id 0")

        svg = SVG(SCRIPT_DIR + '/results/test-regroup-operator-3.svg')
        for shape in new_shapes:
            shape.fill_color = get_sample_group_color(shape.group_id)
            svg.add_shape(shape)
        svg.save_svg()

    def test_regroup4(self):
        """
        test splitting the simple square
        """
        param_values = [
            OperatorParameterValue("k", 4)
        ]
        operator = RegroupOperator(param_values)

        shapes = operator.get_thumbnail_shapes_grid(0.25)

        new_shapes = operator.execute(shapes, [])

        self.assertEqual(new_shapes[0].group_id, 0, "first shape is group id 0")
        self.assertEqual(new_shapes[1].group_id, 1, "second shape is group id 1")
        self.assertEqual(new_shapes[2].group_id, 2, "third shape is group id 2")
        self.assertEqual(new_shapes[3].group_id, 3, "fourth shape is group id 3")
        self.assertEqual(new_shapes[4].group_id, 0, "fifth shape is group id 0")

        svg = SVG(SCRIPT_DIR + '/results/test-regroup-operator-4.svg')
        for shape in new_shapes:
            shape.fill_color = get_sample_group_color(shape.group_id)
            svg.add_shape(shape)
        svg.save_svg()

    def test_regroup_thumbnail(self):
        param_values = [
            OperatorParameterValue("k", 3)
        ]
        operator = RegroupOperator(param_values)
        png_filename = SCRIPT_DIR + '/results/test-regroup-operator-thumbnail.png'
        operator.create_thumbnail(png_filename)

    def test_ungroup(self):
        """
        test splitting the simple square
        """
        param_values = []
        operator = UngroupOperator(param_values)

        shapes = operator.get_thumbnail_shapes_grid(0.25)

        new_shapes = operator.execute(shapes, [])

        self.assertEqual(new_shapes[0].group_id, 0, "first shape is group id 0")
        self.assertEqual(new_shapes[1].group_id, 1, "second shape is group id 1")
        self.assertEqual(new_shapes[2].group_id, 2, "third shape is group id 2")
        self.assertEqual(new_shapes[15].group_id, 15, "16th shape is group id 15")

        svg = SVG(SCRIPT_DIR + '/results/test-ungroup-operator.svg')
        for shape in new_shapes:
            shape.fill_color = get_sample_group_color(shape.group_id)
            svg.add_shape(shape)
        svg.save_svg()


    def test_ungroup_thumbnail(self):
        param_values = [
        ]
        operator = UngroupOperator(param_values)
        png_filename = SCRIPT_DIR + '/results/test-ungroup-operator-thumbnail.png'
        operator.create_thumbnail(png_filename)


if __name__ == '__main__':
    unittest.main()