from zentangler.grammar import Grammar
from zentangler.rule import Rule
from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.split_operator import SplitOperator
from zentangler.operators.operator_parameter import OperatorParameterValue
from zentangler.operators.grouping_operator import RegroupOperator
from zentangler.operators.grouping_operator import UngroupOperator
import json

class GrammarManager:
    """
    Grammar Manager class contains helper methods to create a grammar
    """
    grammar: Grammar

    def __init__(self):
        """
        initialize a tangle

        Parameters:
            shapes: initial set of shapes
            grammar: the grammar to be used to create tangle
        """

    def get_grammar(self, grammar_filepath):

        # open and parse file
        with open(grammar_filepath) as jsonfile:
            grammar_json = json.load(jsonfile)

        grammar = Grammar()
        grammar.name = grammar_json.get("grammar_name")
        grammar.seed = grammar_json.get("seed")
        rules_dict = grammar_json.get("rules")
        grammar.rules = []

        for r in rules_dict:
            new_rule = Rule()

            new_rule.name = r.get("rule_name")

            new_rule.matching_tags = []
            matching_tags_dict = r.get("matching_tags")
            for m in matching_tags_dict:
                new_rule.matching_tags.append(m)

            new_rule.group_id = r.get("group_id")

            new_rule.output_tags = []
            output_tags_dict = r.get("output_tags")
            for o in output_tags_dict:
                new_rule.output_tags.append(o)

            new_rule.parameters = r.get("parameters")

            new_rule.operator = self.get_operator(r.get("operator"), new_rule.parameters)

            grammar.rules.append(new_rule)

        self.grammar = grammar

        return grammar

    def get_operator(self, operator_name, parameters: dict):
        operator = None

        param_values = []
        for p in parameters:
            param_values.append(OperatorParameterValue(p, parameters[p]))

        # todo: add more operators
        if operator_name == "split":
            operator = SplitOperator(param_values)

        if operator_name == "ungroup":
            operator = UngroupOperator(param_values)

        if operator_name == "regroup":
            operator = RegroupOperator(param_values)

        return operator
