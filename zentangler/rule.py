from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.operator_parameter import OperatorParameterValue


class Rule:
    """
    Rule class that holds details of a rule in a grammar
    """
    # name: str
    # operator: AbstractOperator
    # parameters: dict
    # matching_tags: list
    # group_id: int
    # output_tags: list

    def __init__(self, name, operator: AbstractOperator, parameter_values : list, matching_tags : list, group_id, output_tags : list):
        """
        initialize rule

        Parameters:
            name: rule name
            operator: operators the rule applies
            matching_tags: tags that need to match for rule to be applied
            group_id: shape group id that need to match for rule to be applied
            output_tags: tags for the output shapes after rule is applied
        """
        self.name = name
        self.operator = operator
        self.parameter_values: [OperatorParameterValue] = parameter_values
        self.matching_tags = matching_tags
        self.group_id = group_id
        self.output_tags = output_tags

    def set_parameter_value(self, value: OperatorParameterValue):
        self.parameter_values[value.name] = value.value
        self.operator.set_parameter_value(value)

    def get_parameter_value(self, param_name: str):
        if param_name in self.parameter_values:
            return self.parameter_values[param_name]
        else:
            # might have a default set by the operator
            return self.operator.get_parameter_value(param_name)
