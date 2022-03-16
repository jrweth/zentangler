from polygon import Polygon
import copy

class Shape:
    """Represents a shape in the tangle including ids and properties"""
    def __init__(
            self,
            tag: str = "origin",
            group_id: int = 0,
            shape_id: int = 0,
            outer_polygon: Polygon = None,
            inner_polygons: list = [],
            shape_attributes: list = [],
            parent_shape = None
    ):
        """
        initializer for a shape class instance
        Parameters
        ----------
        tag : str
            Name of the shape type referenced by grammar rules
        group_id : int
            Id of the group of shapes
        shape_id : int
            Sequential id of the shape within the group of shapes to which it belongs
        outer_polygon: Polygon
            The definition of the outer polygon for the shape.  Should be defined in a clockwise manner
        inner_polygons: list[Polygon]
            List of interior polygon "holes" in the interior of the outer polygon. Should be defined in counter-clockwise manner
        shape_attributes: list
            List of shape attributes
        parent_shape: Shape
            Direct ancestor shape which created this shape (null for origin shapes)
        """
        self.tag = tag
        self.group_id = group_id
        self.shape_id = shape_id
        self.outer_polygon: Polygon = outer_polygon
        self.inner_polygons: list[Polygon] = inner_polygons
        self.shape_attributes = shape_attributes
        self.parent_shape = parent_shape

    def clone(self):
        """
        Clone this shape into another shape
        """
        return copy.deepcopy(self)
