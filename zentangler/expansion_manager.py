from zentangler.shape import Shape
from zentangler.rule import Rule
from zentangler.expansion import Expansion
from zentangler.grammar import Grammar


class ExpansionManager:
    """
    Expansion Manager class contains helper methods to store the intermediate expansion values
    """
    matched_rule: Rule
    expansion: Expansion
    grammar: Grammar

    def __init__(self, expansion: Expansion):
        """
        initialize a tangle
        """
        self.expansion = expansion

    def match(self, active_shapes, grammar):
        self.grammar = grammar
        # self.expansion = Expansion(None, None, None)
        self.matched_rule = None    # default value

        # get matching random rule
        matched_shape = Shape()
        for shape in active_shapes:
            matched_shape = shape
            if self.match_rule(shape):
                break

        # get shapes to apply rule on
        for shape in active_shapes:
            if shape.group_id == matched_shape.group_id and shape.tag == matched_shape.tag:  # ??: match with just gid or with tag also
                self.expansion.addToMatched(shape)
            else:
                self.expansion.addToRemainder(shape)

        return self

    def match_rule(self, shape):
        matched_rules = []

        for rule in self.grammar.rules:
            if self.tag_in_rule(shape.tag, rule.matching_tags):
                matched_rules.append(rule)

        if matched_rules:
            self.matched_rule = matched_rules[0]  # todo: randomize rule returned
            return True
        else:
            return False

    def tag_in_rule(self, tag, tags: list) -> bool:
        for t in tags:
            if tag == t:
                return True

        return False
