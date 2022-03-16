import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.utils import do_intersect, get_intersect, on_segment
from zentangler.point import Point

class TestUtils(unittest.TestCase):
    def testGetIntersect(self):
        #test points crossing at 0.5
        a = Point(0, 0)
        b = Point(1, 1)
        c = Point(1, 0)
        d = Point(0, 1)

        p = get_intersect(a, b, c, d)
        self.assertEqual(p.x, 0.5, "x is 0.5")
        self.assertEqual(p.y, 0.5, "y is 0.5")

        #test points that are colinear
        a = Point(0, 0)
        b = Point(1, 1)
        c = Point(0.6, 0.6)
        d = Point(1, 1)

        p = get_intersect(a, b, c, d)

        self.assertEqual(p.x, 0.6, "x is 0.6")
        self.assertEqual(p.y, 0.6, "y is 0.6")

        #test points that don't intersect
        a = Point(0, 0)
        b = Point(0, 1)
        c = Point(1, 0)
        d = Point(1, 1)

        p = get_intersect(a, b, c, d)
        self.assertEqual(p, None, "lines don't intersect")


if __name__ == '__main__':
    unittest.main()