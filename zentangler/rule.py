from zentangler.operators.abstract_operator import AbstractOperator


class Rule:
    """
    Rule class that holds details of a rule in a grammar
    """
    name: str
    operator: AbstractOperator
    parameters: dict
    matching_tags: list
    group_id: int
    output_tags: list

    def __init__(self): #, name, operator: AbstractOperator, parameters : list, matching_tags : list, group_id, output_tags : list):
        """
        initialize rule

        Parameters:
            name: rule name
            operator: operators the rule applies
            matching_tags: tags that need to match for rule to be applied
            group_id: shape group id that need to match for rule to be applied
            output_tags: tags for the output shapes after rule is applied
        """
