import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.svg import SVG
from zentangler.shape import Shape
from test_shape import SQUARE_SHAPE
# from zentangler.operators.split_operator import SplitOperator
from zentangler.operators.place_operator import PlaceOperator
from zentangler.operators.operator_parameter import OperatorParameterValue



class TestPlaceOperator(unittest.TestCase):
    def test_ngon_points(self):
        from zentangler.operators.place_operator import ngon_points
        diamond = ngon_points(4)
        self.assertEqual(diamond[0][0], 0.5, "first x coord is 0.5")
        self.assertEqual(diamond[0][1], 0, "first y coord is 0")
        self.assertLess(abs(diamond[1][0]), 0.00001, "second x coord is almost 0")
        self.assertLess(abs(diamond[1][1] - 0.5), 0.00001, "second x coord is almost 0.5")

    def test_basic(self):
        """
        test splitting the simple square and then assigning colors
        """
        shape: Shape = SQUARE_SHAPE.clone()
        param_values = [
            OperatorParameterValue("min_size", 0.1),
            OperatorParameterValue("max_size", 0.1),
            OperatorParameterValue("min_distance", 0.1),
            OperatorParameterValue("random_seed", 2),
            OperatorParameterValue("shape_type", "circle"),
            OperatorParameterValue("num_shape_sides", 5),
            OperatorParameterValue("rotation_random", False),
            OperatorParameterValue("placement_type", "grid"),
        ]
        operator = PlaceOperator(param_values)

        new_shapes: list[Shape] = operator.execute([shape], ['circles', 'remainder'])

        svg = SVG(SCRIPT_DIR + '/results/test-place-operator-basic.svg')
        for shape in new_shapes:
            svg.add_shape(shape)
        svg.save_svg()

        # self.assertEqual(new_shapes[0].stroke_color[0], 1, "red stroke value matches")
        # self.assertEqual(new_shapes[0].fill_color[1], 1, "green fill value matches")
        # self.assertEqual(new_shapes[0].tag, 'colored', "new tag matches")

if __name__ == '__main__':
    unittest.main()