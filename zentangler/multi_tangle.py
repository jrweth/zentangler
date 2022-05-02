import copy

from zentangler.tangle import Tangle
from zentangler.svg import SVG
from zentangler.grammar import BASE_GRAMMARS, Grammar
from zentangler.grammar_manager import GrammarManager

class MultiTangle:
    """
    Class holding multiple tangles that can be rendered into a single image
    """

    def __init__(self, tangles: list = [], tangle_name: str = "multi_tangle"):
        """
        Parameters:
            tangles: list<Tangle>
                list of tangles
        """
        self.tangles: [Tangle] = tangles
        self.tangle_name = tangle_name

    def add_tangle(self, tangle: Tangle):
        """
        Add a tangle to the list of tangles

        Parameters:
            tangle: Tangle
                tangle to add
        """
        self.tangles.append(tangle)


    def init_from_shape_lists_random_grammar(self, shape_lists: list):
        """
        Initialize the multi tangle based upon the list of
        Parameters:
            shape_list: list[list[Shape]]
        """
        index = 0
        grammar_mgr = GrammarManager()
        for shape_list in shape_lists:
            grammar = grammar_mgr.get_random_base_grammar(random_seed=index+6)
            self.add_tangle(Tangle(shape_list, grammar))
            index += 1

    def init_from_shape_lists_cycle_grammars(self, shape_lists: list):
        """
        Initialize the multi tangle based upon the list of shapes lists provided by cycling through base grammars
        Parameters:
            shape_list: list[list[Shape]]
        """
        index = 0
        grammar_mgr = GrammarManager()
        for i in range(len(shape_lists)):
            grammar_base_index = index % len(BASE_GRAMMARS)
            grammar = grammar_mgr.get_grammar(BASE_GRAMMARS[grammar_base_index]["path"])
            sub_name = self.tangle_name + "_" + str(i)
            self.add_tangle(Tangle(shape_lists[i], grammar, sub_name))
            index += 1

    def init_from_shape_lists_grammar(self, shape_lists: list, grammar: Grammar):
        """
        Initialize the multi tangle based upon the list of shapes lists provided by picking random base grammars
        """
        for shape_list in shape_lists:
            grammar_clone = copy.deepcopy(grammar)
            self.add_tangle(Tangle(shape_list, grammar_clone))


    def init_from_shape_lists_grammar_file(self, shape_lists: list, grammar_filepath: str):
        """
        Initialize the multi tangles based upon a list of shape lists, and a grammar
        """
        for shape_list in shape_lists:
            grammar = Grammar()
            grammar.load_from_file(grammar_filepath)
            self.add_tangle(Tangle(shape_list, grammar))



    def create_all(self):
        """
        Create all the tangles by running the expansion
        """
        for tangle in self.tangles:
            tangle.create()


    def re_expand_all(self):
        """
        Re-expand all of the
        """
        for tangle in self.tangles:
            tangle.re_expand()

    def re_expand_one(self, tangle_index):
        """
        re_expand the tangle at the given index
        """
        self.tangles[tangle_index].re_expand()

    def move_to_back(self, tangle_index):
        """
        move the tangle at the given index to the back (index 0)
        Parameters:
            tangle_index:
                the tangle_index of the tangle to move to the back
        """
        new_tangle_order = [self.tangles[tangle_index]]
        for i in range(0, tangle_index):
            new_tangle_order.append(self.tangles[i])
        self.tangles = new_tangle_order

    def move_to_front(self, tangle_index):
        """
        move the tangle at the given index to the front (index 0)
        Parameters:
            tangle_index:
                the tangle_index of the tangle to move to the front
        """
        tangle = self.tangles[tangle_index]
        new_tangle_order = []
        for i in range(0, len(self.tangles)):
            if not i == tangle_index:
                new_tangle_order.append(self.tangles[i])
        new_tangle_order.append(tangle)
        self.tangles = new_tangle_order

    def create_combined_svg(self, svg_filename):
        """
        create a combined svg of all the tangle shapes created in order
        """
        svg = SVG(svg_filename)
        for shape in self.get_last_expansion_shapes():
            svg.add_shape(shape)
        svg.save_svg()

    def create_combined_png(self, png_filename, resolution=2048):

        svg_filename = png_filename.replace('.png', '.svg').replace('.PNG', '.SVG')
        svg = SVG(svg_filename)
        for shape in self.get_last_expansion_shapes():
            svg.add_shape(shape)
        svg.save_png(png_filename, resolution)


    def get_last_expansion_shapes(self):
        shapes = []
        for tangle in self.tangles:
            for shape in tangle.get_last_expansion_shapes():
                shapes.append(shape)
        return shapes
