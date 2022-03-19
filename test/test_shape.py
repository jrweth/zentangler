import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.shape import Shape
from test_polygon import SQUARE_POLYGON

SQUARE_SHAPE: Shape = Shape(
    tag="origin",
    group_id=0,
    shape_id=0,
    geometry=SQUARE_POLYGON,
    parent_shape=None,
    shape_attributes=[]
)

class TestShape(unittest.TestCase):
    global SQUARE_SHAPE
    def test_clone(self):
        cloned: Shape = SQUARE_SHAPE.clone()
        self.assertEqual(cloned.geometry.geoms[0].exterior.coords[0][0], SQUARE_POLYGON.geoms[0].exterior.coords[0][0], "cloned shape point matches")

if __name__ == '__main__':
    unittest.main()