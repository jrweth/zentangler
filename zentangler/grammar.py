import os
import random
from zentangler.operators.grouping_operator import UngroupOperator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_GRAMMARS = [
    {
        "name": "Base Grammar 1",
        "path": SCRIPT_DIR + "/grammars/test_grammar_1.json",
        "icon_path": SCRIPT_DIR + "/grammars/test_grammar_1.png",
    },
    {
        "name": "Base Grammar 2",
        "path": SCRIPT_DIR + "/grammars/test_grammar_2.json",
        "icon_path": SCRIPT_DIR + "/grammars/test_grammar_2.png",
    },
    {
        "name": "Base Grammar 3",
        "path": SCRIPT_DIR + "/grammars/test_grammar_3.json",
        "icon_path": SCRIPT_DIR + "/grammars/test_grammar_3.png",
    }
]

class Grammar:
    """
    Grammar class that holds details of a grammar
    """
    name: str
    rules: list
    seed: int

    def __init__(self): #, name, rules: list, seed):
        """
        initialize a grammar

        Parameters:
            name: grammar name
            rules: list of all the rules in the grammar
            seed: random number generator seed
        """
        # self.name = name
        # self.rules = rules      # ??: should rules be a map
        # self.seed = seed

    def load_from_file(self, filename):
        op = UngroupOperator()
        self.operators.push(op)

    def load_from_string(self, grammar_string):
        op = UngroupOperator()
        self.operators.push(op)



