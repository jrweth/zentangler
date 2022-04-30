import sys
import os
os.system("export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib")

from zentangler.tangle import Tangle
from zentangler.grammar import Grammar
from zentangler.shape import Shape
from shapely.geometry import MultiPolygon
from zentangler.svg import SVG
from zentangler.grammar_manager import GrammarManager
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


def main():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    grammar_filepath = SCRIPT_DIR + "/grammars/test_grammar_1.json"

    print(os.getcwd())

    grammarManager = GrammarManager()
    # parse grammar & rules
    grammar = grammarManager.get_grammar(grammar_filepath)

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
    svg = SVG(SCRIPT_DIR + '/results/test-2.svg')
    for shape in tangle_shapes:
        svg.add_shape(shape)
    svg.save_svg()

    # convert SVG to PNG

    return 1


main()
