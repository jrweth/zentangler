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

class TestGrammar(unittest.TestCase):
    def test_grammar_1(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_1.json"))
        self.assertEqual(len(grammar.rules), 3, "There are 3 grammar rules")
        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar1.svg')

        self.assertEqual(len(tangle.grammar.rules), 3, "number of grammar rules is 3")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 337)

    def test_grammar_2(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_2.json"))

        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar2.svg')

        self.assertEqual(len(grammar.rules), 5, "There are 5 grammar rules")
        self.assertEqual(len(tangle.grammar.rules), 5, "number of grammar rules is 5")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 291)


    def test_grammar_3(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_3.json"))

        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar3.svg')

        # self.assertEqual(len(grammar.rules), 5, "There are 5 grammar rules")
        # self.assertEqual(len(tangle.grammar.rules), 5, "number of grammar rules is 5")
        # self.assertEqual(len(tangle.get_last_expansion_shapes()), 291)


if __name__ == '__main__':
    unittest.main()