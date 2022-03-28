from zentangler.operators.ungroup_operator import UngroupOperator
from zentangler.rule import Rule
from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.split_operator import SplitOperator
from zentangler.operators.operator_parameter import OperatorParameterValue
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

            matching_tags_dict = r.get("matching_tags")
            for m in matching_tags_dict:
                new_rule.matching_tags.append(m)

            new_rule.group_id = r.get("group_id")

            output_tags_dict = r.get("output_tags")
            for o in output_tags_dict:
                new_rule.output_tags.append(o)

            parameter_dict = r.get("parameters")
            for p in parameter_dict:
                new_rule.parameters.append(p)

            new_rule.operator = self.get_operator(r.get("operators"), new_rule.parameters)

            grammar.rules.append(new_rule)

        return grammar

    def get_operator(self, operator_name, parameters: list):
        operator = None

        # todo: add more operators
        if operator_name == "split":
            param_values = [
                OperatorParameterValue("width", parameters[0]),
                OperatorParameterValue("angle", parameters[1])
            ]
            operator = SplitOperator(param_values)

        return operator
