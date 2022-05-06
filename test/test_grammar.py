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
        self.assertEqual(len(grammar.rules), 4, "There are 4 grammar rules")
        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar1.svg')
        tangle.create_last_expansion_png(os.path.dirname(SCRIPT_DIR) + '/zentangler/grammars/test_grammar_1.png', 100)

        self.assertEqual(len(tangle.grammar.rules), 4, "number of grammar rules is 4")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 337)

    def test_grammar_2(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_2.json"))

        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar2.svg')
        tangle.create_last_expansion_png(os.path.dirname(SCRIPT_DIR) + '/zentangler/grammars/test_grammar_2.png', 100)

        self.assertEqual(len(grammar.rules), 5, "There are 5 grammar rules")
        self.assertEqual(len(tangle.grammar.rules), 5, "number of grammar rules is 5")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 291)


    def test_grammar_3(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_3.json"))

        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar3.svg')
        tangle.create_last_expansion_png(os.path.dirname(SCRIPT_DIR) + '/zentangler/grammars/test_grammar_3.png', 100)

        self.assertEqual(len(grammar.rules), 9, "There are 9 grammar rules")
        self.assertEqual(len(tangle.grammar.rules), 9, "number of grammar rules is 9")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 138)

    def test_grammar_4(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_4.json"))

        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar4.svg')
        tangle.create_last_expansion_png(os.path.dirname(SCRIPT_DIR) + '/zentangler/grammars/test_grammar_4.png', 100)

        self.assertEqual(len(grammar.rules), 16, "There are 16 grammar rules")
        self.assertEqual(len(tangle.grammar.rules), 16, "number of grammar rules is 16")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 451)

    def test_grammar_5(self):
        gm = GrammarManager()
        grammar = gm.get_grammar((os.path.dirname(SCRIPT_DIR) + "/zentangler/grammars/test_grammar_5.json"))

        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar5.svg')
        tangle.create_last_expansion_png(os.path.dirname(SCRIPT_DIR) + '/zentangler/grammars/test_grammar_5.png', 100)

        self.assertEqual(len(grammar.rules), 18, "There are 18 grammar rules")
        self.assertEqual(len(tangle.grammar.rules), 18, "number of grammar rules is 18")
        self.assertEqual(len(tangle.get_last_expansion_shapes()), 118)

    def test_grammar_random(self):
        gm = GrammarManager()
        grammar = gm.get_random_base_grammar()

        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])

        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar-random.svg')

        grammar = gm.get_random_base_grammar(53)
        tangle = Tangle(grammar=grammar, init_shapes=[SQUARE_SHAPE])
        tangle.create()
        tangle.create_last_expansion_svg(SCRIPT_DIR + '/results/test-grammar-random2.svg')

if __name__ == '__main__':
    unittest.main()