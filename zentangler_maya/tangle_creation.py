import os
from shapely.geometry import MultiPolygon
from zentangler.shape import Shape
from zentangler.tangle import Tangle
from zentangler.grammar_manager import GrammarManager

def create_silhouette_tangle(object, grammar_filename, override_png_filename = None):
    if override_png_filename == None:
        png_filename = "some filename"
    else:
        png_filename = "override_png_filename"

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    grammar_filepath = SCRIPT_DIR + "/grammars/test_grammar_1.json"

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
    tangle = Tangle(initial_shapes, grammar_filename)
    return {"tangle": tangle, "png_filename": png_filename}

def create_uv_map_tangle(object, grammar_filename, override_png_filename = None):
    if override_png_filename == None:
        png_filename = "some filename"
    else:
        png_filename = "override_png_filename"

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    grammar_filepath = SCRIPT_DIR + "/grammars/test_grammar_1.json"

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
    tangle = Tangle(initial_shapes, grammar_filename)
    return {"tangle": tangle, "png_filename": png_filename}
