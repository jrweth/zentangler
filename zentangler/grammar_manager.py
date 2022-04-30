from zentangler.grammar import Grammar, BASE_GRAMMARS
from zentangler.rule import Rule
from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.split_operator import SplitOperator
from zentangler.operators.operator_parameter import OperatorParameterValue
from zentangler.operators.grouping_operator import RegroupOperator
from zentangler.operators.grouping_operator import UngroupOperator
from zentangler.operators.color_operator import ColorOperator
from zentangler.operators.line_width_operator import LineWidthOperator
from zentangler.operators.place_operator import PlaceOperator
from zentangler.operators.operator_parameter import ParameterDataType
import json
import random

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
            rule_name = r.get("rule_name")

            matching_tags = []
            matching_tags_dict = r.get("matching_tags")
            for m in matching_tags_dict:
                matching_tags.append(m)

            group_id = r.get("group_id")

            output_tags = []
            output_tags_dict = r.get("output_tags")
            for o in output_tags_dict:
                output_tags.append(o)

            parameters = r.get("parameters")

            operator = self.get_operator(r.get("operator"), parameters)

            for param_name in parameters:
                parameters[param_name] = self.adjust_param_value_for_datatype(
                    operator,
                    param_name,
                    parameters[param_name]
                )

            new_rule = Rule(
                rule_name,
                operator,
                parameters,
                matching_tags,
                group_id,
                output_tags
            )
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

        elif operator_name == "ungroup":
            operator = UngroupOperator(param_values)

        elif operator_name == "regroup":
            operator = RegroupOperator(param_values)

        elif operator_name == "color":
            operator = ColorOperator(param_values)

        elif operator_name == "line_width":
            operator = LineWidthOperator(param_values)

        elif operator_name == "place":
            operator = PlaceOperator(param_values)

        return operator

    def get_random_base_grammar(self, random_seed=1):
        random.seed(random_seed)
        base_grammar_index = random.randint(0, len(BASE_GRAMMARS)-1)
        base_grammar_def = BASE_GRAMMARS[base_grammar_index]
        return self.get_grammar(base_grammar_def["path"])

    def adjust_param_value_for_datatype(self, operator: AbstractOperator, param_name: str, param_value):
        """
        adjust the parameter value based on the expected data type
        """
        param_def = operator.get_parameter_definition(param_name)
        if param_def and param_def.data_type == ParameterDataType.RGB_COLOR:
            if param_def.is_multiple:
                colors = []
                for value in param_value:
                    colors.append((value[0], value[1], value[2]))
                return colors
            else:
                return (param_value[0], param_value[1], param_value[2])
        return param_value
