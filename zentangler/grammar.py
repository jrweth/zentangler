from zentangler.operator.ungroup_operator import UngroupOperator
from zentangler.rule import Rule
import json


class Grammar:
    """
    Grammar class that holds details of a grammar
    """

    def __init__(self, name, rules: list, seed):
        """
        initialize a grammar

        Parameters:
            name: grammar name
            rules: list of all the rules in the grammar
            seed: random number generator seed
        """
        self.name = name
        self.rules = rules      # ??: should rules be a map
        self.seed = seed

    def load_from_file(self, filename):
        op = UngroupOperator()
        self.operators.push(op)

    def load_from_string(self, grammar_string):
        op = UngroupOperator()
        self.operators.push(op)

    def get_grammar(self, filename):

        # open and parse file
        with open(filename) as jsonfile:
            grammar_json = json.load(jsonfile)

        grammar = Grammar()
        grammar.name = grammar_json.get("name")
        grammar.seed = grammar_json.get("seed")
        rules_dict = grammar_json.get("rules")

        for r in rules_dict:
            new_rule = Rule()

            new_rule.name = r.get("name")
            new_rule.matching_tags = r.get("matching_tags")
            new_rule.group_id = r.get("group_id")
            new_rule.output_tags = r.get("output_tags")
            new_rule.parameters = r.get("parameters")

            grammar.rules.append(new_rule)

        return grammar
