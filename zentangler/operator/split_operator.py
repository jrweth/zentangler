from math import cos, sin

import shapely.geometry

from zentangler.operator.abstract_operator import AbstractOperator
from zentangler.shape import Shape
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely import wkt

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
        self.output_tags = output_tags
        new_shapes = []
        for shape in shapes:
            new_shapes.extend(self.split_shape(shape))

        return new_shapes

    def split_shape(self, shape) -> list:
        """
        will take a shape and bisect it via parralel strips
        """
        x = 0
        y = 0
        new_shapes = []
        # loop through x and y
        while x < 1 and y < 1:
            y += self.width
            strip = Polygon([(x, y), (1, y), (1, y + self.width), (x, y + self.width)])
            new_polys = []
            for i in range(0, len(shape.geometry.geoms)):
                intersection = strip.intersection(shape.geometry.geoms[i])
                if intersection:
                    #check out what type of intersection object is returned and extract the polygons from it
                    if isinstance(intersection, Polygon):
                        new_polys.append(intersection)
                    elif isinstance(intersection, MultiPolygon):
                        for poly in intersection.geoms:
                            new_polys.append(poly)
                    elif isinstance(intersection, GeometryCollection):
                        for geo in intersection.geoms:
                            if isinstance(geo, Polygon):
                                new_polys.append(geo)
                    else:
                        print(intersection)


            if(new_polys):
                multi = MultiPolygon(new_polys)
                new_shape = Shape(geometry=multi)
                new_shape.parent_shape = shape
                new_shape.tag = self.output_tags[0]
                new_shapes.append(new_shape)
        return new_shapes
