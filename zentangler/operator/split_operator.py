from abstract_operator import AbstractOperator
from zentangler.shape import Shape

class SplitOperator(AbstractOperator):
    """
    Operator which splits a shape into regular shapes
    """
    def __init__(self, width: float = 0.1, orientation: float = 0.0, cross: bool = False):
        self.width = width
        self.orientation = orientation
        self.cross = cross

    def execute(self, shape: Shape) -> list:
        new_shape = shape.clone()
        new_shape.parent_shape = shape
        shapes = [new_shape]
        return shapes


split = SplitOperator(width=0.1, orientation=45, cross=True)
