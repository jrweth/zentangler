from zentangler.operator.ungroup_operator import UngroupOperator
from zentangler.rule import Rule

class Grammar:
    """
    Grammar class that holds details of a grammar
    """

    def __init__(self, name, rules : list[Rule], seed):
        """
        initialize a grammar

        Parameters:
            name: grammar name
            rules: list of all the rules in the grammar
            seed: random number generator seed
        """
        self.name = name
        self.rules = rules
        self.seed = seed

    def load_from_file(self, filename):
        op = UngroupOperator()
        self.operators.push(op)

    def load_from_string(self, grammar_string):
        op = UngroupOperator()
        self.operators.push(op)

    def get_grammar(self, filename):
        # load file
        # parse file

        grammar = Grammar()
        grammar.name = "name"

        return grammar
