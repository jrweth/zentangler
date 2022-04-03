from zentangler.expansion import Expansion
from zentangler.expansion_manager import ExpansionManager
from grammar import Grammar
from shape import Shape


class Tangle:
    """
    Tangle class holds the tangle creation (grammar expansion) logic
    """
    """
    Parameters:
        history: collection of expansions to define how the tangle was generated
    """
    history: list

    def __init__(self, init_shapes: list, grammar: Grammar):
        """
        initialize a tangle

        Parameters:
            init_shapes: initial set of shapes
            grammar: the grammar to be used to create tangle
        """
        self.all_shapes = init_shapes
        self.grammar = grammar

    def create(self):   #, init_shapes: list, grammar: Grammar):
        print("Creating tangle")

        # self.grammar = grammar
        # self.shapes = init_shapes

        # save starting shapes
        self.history = []
        self.history.append(Expansion(self.all_shapes, None, None))

        step = 0
        while self.expand():
            print("Expansion step " + str(step))
            step += 1

        print("Ending tangle")

    def expand(self):

        # get last expansion
        last_expansion = self.history[-1]
        active_shapes = last_expansion.shapes

        # find matching rule and shapes
        expansion_step = ExpansionManager(Expansion(None, None, None))
        expansion_step = expansion_step.match(active_shapes, self.grammar)

        if expansion_step.matched_rule is None:
            return False

        # apply operators to shapes
        matched_operator = expansion_step.matched_rule.operator
        expansion_step.expansion.added = matched_operator.execute(expansion_step.expansion.matched,
                                                                  expansion_step.matched_rule.output_tags)

        expansion_step.expansion.appendAllShapes()
        # append expansion to history
        self.history.append(expansion_step.expansion)

        return True
