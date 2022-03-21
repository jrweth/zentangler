#from zentangler.operator import AbstractOperator   ??: cannot use an abstract class


class Rule:
    """
    Rule class that holds details of a rule in a grammar
    """
    def __init__(self, name, operator, parameters : list, matching_tags : list, group_id, output_tags : list):
        """
        initialize rule

        Parameters:
            name: rule name
            operator: operator the rule applies
            matching_tags: tags that need to match for rule to be applied
            group_id: shape group id that need to match for rule to be applied
            output_tags: tags for the output shapes after rule is applied
        """
        self.name = name
        self.operator = operator
        self.parameters = parameters
        self.matching_tags = matching_tags
        self.group_id = group_id
        self.output_tags = output_tags
