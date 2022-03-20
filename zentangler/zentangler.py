from zentangler.tangle import Tangle
from zentangler.grammar import Grammar
from shape import Shape
from zentangler.svg import SVG
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
grammar_filepath = SCRIPT_DIR + "/grammars/test_grammar_1.json"


def main():
    # parse grammar & rules
    grammar = Grammar.get_grammar(grammar_filepath)

    # create tangle
    tangle_shapes = Tangle.create(grammar)

    # use shapes to create SVG
    svg = SVG(SCRIPT_DIR + '/results/test-1.svg')
    for shape in tangle_shapes:
        svg.add_shape(shape)
    svg.save_svg()

    # convert SVG to PNG

    return 1
