from zentangler.tangle import Tangle
from zentangler.grammar import Grammar
from zentangler.shape import Shape
from shapely.geometry import MultiPolygon
from zentangler.svg import SVG
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
grammar_filepath = SCRIPT_DIR + "/grammars/test_grammar_1.json"


def main():
    # parse grammar & rules
    grammar = Grammar.get_grammar(grammar_filepath)

    initial_shapes = [Shape(
        tag="origin",
        group_id=0,
        shape_id=0,
        geometry=MultiPolygon([
            [[(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], []]
        ]),
        parent_shape=None,
        shape_attributes=[]
    )]

    # create tangle
    tangle = Tangle(initial_shapes, grammar)
    tangle_shapes = tangle.create()

    # use shapes to create SVG
    svg = SVG(SCRIPT_DIR + '/results/test-1.svg')
    for shape in tangle_shapes:
        svg.add_shape(shape)
    svg.save_svg()

    # convert SVG to PNG

    return 1
