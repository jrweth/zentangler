from zentangler.expansion import Expansion
from zentangler.expansion_manager import ExpansionManager
from zentangler.grammar import Grammar
from zentangler.operators.operator_parameter import OperatorParameterValue


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
        self.rule_ids_updated = set()

    def create(self):   #, init_shapes: list, grammar: Grammar):
        print("Creating tangle")

        # self.grammar = grammar
        # self.shapes = init_shapes

        # save starting shapes
        self.history = []
        self.history.append(Expansion(None, self.all_shapes, None))
        print("Expansion step: 0 " + " num shapes: " + str(len(self.all_shapes)))

        step = 0
        while self.expand():
            step += 1
            print("Expansion step: " + str(step) + " num shapes: " + str(len(self.history[-1].getShapesForNewExpansion())))

        print("Ending tangle")

        return self.history[-1].getShapesForNewExpansion()

    def expand(self):

        # get last expansion
        last_expansion: Expansion = self.history[-1]
        active_shapes = last_expansion.getShapesForNewExpansion()

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

    def re_expand(self):
        """
        re_expand the tangle - at this point we will start from the beginning but we might be able to optimize
        """
        self.create()
        self.rule_ids_updated = set()

    def get_last_expansion_shapes(self):
        """
        Return all shapes in tangle after the last expansion
        """
        return self.history[-1].getShapesForNewExpansion()

    def create_last_expansion_svg(self, svg_filename):
        """
        function to output the last expansion to an svg
        Parameters:
            svg_filename: str
                name of the svg file (should end in .svg)
        """
        last_expansion = self.history[-1]
        last_expansion.createExpansionSVG(svg_filename)

    def create_last_expansion_png(self, png_filename, resolution: int = 1024):
        """
        function to output the last expansion to a png
        Parameters:
            png_filename: str
                name of the png file (should end in .png)
        """
        last_expansion = self.history[-1]
        last_expansion.createExpansionPNG(png_filename, resolution)

    def update_rule_parameter(self, rule_id: int, parameterValue: OperatorParameterValue):
        """
        update a rule parameter
        Parameters:
            rule_id: int
                the index of the rule to be updated
            parameterValue: OperatorParameterValue
                the parameter value to be updated
        """
        self.rule_ids_updated.add(rule_id)
        self.grammar.rules[rule_id].operator.set_parameter_value(parameterValue)