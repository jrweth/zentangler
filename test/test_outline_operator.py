import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from test_shape import SQUARE_SHAPE
from test_polygon import HOLED_POLYGON, HOLE_POLYGON
from zentangler.shape import Shape
from zentangler.operators.outline_operator import OutlineOperator
from zentangler.svg import SVG
from zentangler.operators.operator_parameter import OperatorParameterValue

class TestOutlineOperator(unittest.TestCase):

    def test_polygon_is_clockwise(self):
        points = [(0,0), (0, 1), (1, 1), (1, 0)]
        self.assertFalse(OutlineOperator.polygon_is_clockwise(points), "counter clockwise polygon not clockwise")

        points = [(0,0), (1, 0), (1, 1), (0, 1)]
        self.assertTrue(OutlineOperator.polygon_is_clockwise(points), "clockwise polygon is clockwise")


    def test_square_simple(self):
        """
        test splitting the simple square
        """
        shape: Shape = SQUARE_SHAPE.clone()
        param_values = [
            OperatorParameterValue("width", 0.1)
        ]
        operator = OutlineOperator(param_values)

        newShapes: list[Shape] = operator.execute([shape], ['outline', 'remainder'])
        self.assertEqual(len(newShapes), 2, "number of outlined shapes")
        self.assertEqual(newShapes[0].tag, "outline", "new tag name should equal outline")
        self.assertEqual(newShapes[1].tag, "remainder", "new tag name should equal outline")

        svg = SVG(SCRIPT_DIR + '/results/test-outline-operator-simple.svg')
        for shape in newShapes:
            if shape.tag == "remainder":
                shape.fill_color = (1, 0, 0)
            svg.add_shape(shape)
        svg.save_svg()

    def test_square_hole(self):

        shape: Shape = Shape(geometry=HOLE_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.04)
        ]
        operator = OutlineOperator(param_values)

        newShapes: list[Shape] = operator.execute([shape], ['outline', 'remainder'])
        self.assertEqual(len(newShapes), 3, "number of outline shapes is what is expected")
        self.assertEqual(newShapes[0].tag, "outline", "new tag name should equal outline")
        self.assertEqual(newShapes[1].tag, "remainder", "new tag name should equal remainder")
        self.assertEqual(newShapes[2].tag, "outline", "new tag name should equal outline")
        self.assertEqual(newShapes[2].shape_id, 1, "shape id matches for second outline element")

        svg = SVG(SCRIPT_DIR + '/results/test-outline-operator-hole.svg')
        for shape in newShapes:
            if shape.tag == "remainder":
                shape.fill_color = (1, 0, 0)
            svg.add_shape(shape)
        svg.save_svg()


    def test_square_holes(self):

        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.015)
        ]
        operator = OutlineOperator(param_values)

        newShapes: list[Shape] = operator.execute([shape], ['outline', 'remainder'])
        self.assertEqual(len(newShapes), 4, "number of outline shapes is what is expected")
        self.assertEqual(newShapes[0].tag, "outline", "new tag name should equal outline")
        self.assertEqual(newShapes[1].tag, "remainder", "new tag name should equal remainder")
        self.assertEqual(newShapes[2].tag, "outline", "new tag name should equal outline")
        self.assertEqual(newShapes[2].shape_id, 1, "shape id matches for second outline element")
        self.assertEqual(newShapes[3].tag, "outline", "new tag name should equal outline")
        self.assertEqual(newShapes[3].shape_id, 2, "shape id matches for third outline element")

        svg = SVG(SCRIPT_DIR + '/results/test-outline-operator-holes.svg')
        for shape in newShapes:
            if shape.tag == "remainder":
                shape.fill_color = (1, 0, 0)
            svg.add_shape(shape)
        svg.save_svg()


    def test_square_holes2(self):

        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.04)
        ]
        operator = OutlineOperator(param_values)

        newShapes: list[Shape] = operator.execute([shape], ['outline', 'remainder'])
        self.assertEqual(len(newShapes), 3, "number of outline shapes is what is expected")
        self.assertEqual(newShapes[0].tag, "outline", "new tag name should equal outline")
        self.assertEqual(newShapes[1].tag, "remainder", "new tag name should equal remainder")

        svg = SVG(SCRIPT_DIR + '/results/test-outline-operator-holes2.svg')
        for shape in newShapes:
            if shape.tag == "remainder":
                shape.fill_color = (1, 0, 0)
            svg.add_shape(shape)
        svg.save_svg()


    def test_square_holes3(self):
        shape: Shape = Shape(geometry=HOLED_POLYGON)
        param_values = [
            OperatorParameterValue("width", 0.07)
        ]
        operator = OutlineOperator(param_values)

        newShapes: list[Shape] = operator.execute([shape], ['outline', 'remainder'])
        self.assertEqual(len(newShapes), 2, "number of outline shapes is what is expected")
        self.assertEqual(newShapes[0].tag, "outline", "new tag name should equal outline")
        self.assertEqual(newShapes[1].tag, "remainder", "new tag name should equal remainder")

        svg = SVG(SCRIPT_DIR + '/results/test-outline-operator-holes3.svg')
        for shape in newShapes:
            if shape.tag == "remainder":
                shape.fill_color = (1, 0, 0)
            svg.add_shape(shape)
        svg.save_svg()

    def test_thumbnail(self):
        param_values = [
            OperatorParameterValue("width", 0.07)
        ]
        operator = OutlineOperator(param_values)
        png_filename = SCRIPT_DIR + '/results/test-outline-operator-thumbnail.png'
        operator.create_thumbnail(png_filename)

if __name__ == '__main__':
    unittest.main()