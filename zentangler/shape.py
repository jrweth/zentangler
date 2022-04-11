from shapely.geometry import MultiPolygon
import copy

class Shape:
    """Represents a shape in the tangle including ids and properties"""
    def __init__(
            self,
            tag: str = "origin",
            group_id: int = 0,
            shape_id: int = 0,
            geometry: MultiPolygon = None,
            shape_attributes: list = [],
            parent_shape = None,
            stroke_width: float = 0.01,
            stroke_color: () = (0, 0, 0),
            fill_color: () = (0.9, 0.9, 0.9)
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
        geometry: Polygon
            The definition of the outer polygon for the shape
        inner_polygons: list[Polygon]
            List of interior polygon "holes" in the interior of the outer polygon. Should be defined in counter-clockwise manner
        shape_attributes: list
            List of shape attributes
        parent_shape: Shape
            Direct ancestor shape which created this shape (null for origin shapes)
        stroke_width: float
            width of the stroke to draw the shape
        stroke_color: str
            color of the stroke (svg colors e.g. #FFFFFF or white)
        fill_color: str
            color of the fill (svg colors e.g. #FFFFFF or white)
        """
        self.tag = tag
        self.group_id = group_id
        self.shape_id = shape_id
        self.geometry: MultiPolygon = geometry
        self.shape_attributes = shape_attributes
        self.parent_shape = parent_shape
        self.fill_color = fill_color
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color

    def clone(self):
        """
        Clone this shape into another shape
        """
        return copy.deepcopy(self)
