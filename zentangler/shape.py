from polygon import Polygon
class Shape:
    """Represents a shape in the tangle including ids and properties"""
    outer_polygon = Polygon()
    inner_polygons = list[Polygon]