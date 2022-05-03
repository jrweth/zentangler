import unittest
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zentangler.tangle import  Tangle
from zentangler.grammar_manager import GrammarManager
from test_shape import SQUARE_SHAPE
from zentangler.operators.operator_parameter import OperatorParameterValue

class TestTangle(unittest.TestCase):
    def test_tangle(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_1.json"))
        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-tangle.svg')

        self.assertEqual(len(tangle.grammar.rules), 4, "number of grammar rules is 4")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 337)


    def test_re_expand(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_1.json"))
        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()

        self.assertEqual(len(tangle.grammar.rules), 4, "number of grammar rules is 4")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 337)

        tangle.update_rule_parameter(3, OperatorParameterValue("width", 0.03))
        tangle.re_expand()

        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-tangle-re-expand.svg')

        self.assertEqual(len(tangle.grammar.rules), 4, "number of grammar rules is 4")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 251)


if __name__ == '__main__':
    unittest.main()