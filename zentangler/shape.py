from polygon import Polygon
class Shape:
    """Represents a shape in the tangle including ids and properties"""
    def __init__(self, outer_polygon: Polygon = None, inner_polygons: list = []):
        self.outer_polygon: Polygon = outer_polygon
        self.inner_polygons: list[Polygon] = inner_polygons