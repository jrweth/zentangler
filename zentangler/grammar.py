import os
import random
from zentangler.operators.grouping_operator import UngroupOperator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_GRAMMARS = [
    {
        "name": "Base Grammar 1",
        "path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_1.json",
        "icon_path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_1.png",
    },
    {
        "name": "Base Grammar 2",
        "path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_2.json",
        "icon_path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_2.png",
    },
    {
        "name": "Base Grammar 3",
        "path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_3.json",
        "icon_path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_3.png",
    },
    {
        "name": "Base Grammar 4",
        "path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_4.json",
        "icon_path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_4.png",
    },
    {
        "name": "Base Grammar 5",
        "path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_5.json",
        "icon_path": SCRIPT_DIR + os.path.sep + "grammars" + os.path.sep + "test_grammar_5.png",
    }
]

class Grammar:
    """
    Grammar class that holds details of a grammar
    """

    def __init__(self): #, name, rules: list, seed):
        """
        initialize a grammar
        """
        self.name: str = ""
        self.rules: list = []
        self.seed: int = 1




