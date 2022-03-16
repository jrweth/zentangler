from abstract_operator import AbstractOperator
from zentangler.shape import Shape

class SplitOperator(AbstractOperator):

    num_output_tags: int = 1
    """
    Operator which splits a shape into regular shapes
    """
    def __init__(self, width: float = 0.1, orientation: float = 0.0, cross: bool = False):
        self.width = width
        self.orientation = orientation
        self.cross = cross

    def execute(self, shapes: list, output_tags: list) -> list:
        new_shapes = []
        for shape in shapes:
            new_shape = shape.clone()
            new_shape.parent_shape = shape
            new_shape.tag = output_tags[0]
            new_shapes.append(new_shape)

        return new_shapes

