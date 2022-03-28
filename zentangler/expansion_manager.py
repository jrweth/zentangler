from zentangler.shape import Shape
from zentangler.rule import Rule
from zentangler.expansion import Expansion


class ExpansionManager:
    """
    Expansion Manager class contains helper methods to store the intermediate expansion values
    """
    matched_rule: Rule
    expansion: Expansion

    def __init__(self, grammar):
        """
        initialize a tangle

        Parameters:
            shapes: initial set of shapes
            grammar: the grammar to be used to create tangle
        """
        self.grammar = grammar

    def match(self, active_shapes, grammar):
        self.grammar = grammar

        # get matching random rule
        matched_shape = Shape()
        for shape in active_shapes:
            self.match_rule(shape)
            matched_shape = shape

        # get shapes to apply rule on
        for shape in active_shapes:
            if shape.group_id == matched_shape.group_id:  # ??: match with just gid or with tag also
                self.expansion.matched.append(shape)
            else:
                self.expansion.remainder.append(shape)

        return Expansion(self.expansion.matched, self.expansion.added, self.expansion.remainder)

    def match_rule(self, shape):
        matched_rules = []

        for rule in self.grammar.rules:
            if self.tag_in_rule(shape.tag, rule.matching_tags):
                matched_rules.append(rule)

        if matched_rules:
            self.matched_rule = matched_rules[0]  # todo: randomize rule returned
        else:
            self.matched_rule = None    # ??: not sure how to handle

    def tag_in_rule(self, tag, tags: list) -> bool:
        for t in tags:
            if tag == t:
                return True

        return False
