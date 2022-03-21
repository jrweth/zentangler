from zentangler.expansion import Expansion
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
        self.shapes = init_shapes
        self.grammar = grammar

    def create(self, grammar: Grammar):

        # save current shapes

        # expand loop start
            # fetch shapes
            # match rule
            # apply rule
            # save expansion
        # end loop

        return 1

