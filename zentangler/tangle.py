from grammar import Grammar
from shape import Shape
class Tangle:
    def __init__(self, init_shapes: list[Shape], grammar: Grammar):
        self.shapes = init_shapes
        self.gramamr = grammar