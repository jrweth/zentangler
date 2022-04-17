import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.tangle import  Tangle
from zentangler.grammar_manager import GrammarManager
from test_shape import SQUARE_SHAPE

class TestTangle(unittest.TestCase):
    def testTangle(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_1.json"))
        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()


if __name__ == '__main__':
    unittest.main()