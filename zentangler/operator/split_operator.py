from math import cos, sin

import shapely.geometry

from zentangler.operator.abstract_operator import AbstractOperator
from zentangler.operator.operator_parameter import OperatorParameter, ParameterDataType
from zentangler.shape import Shape
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely import wkt

class SplitOperator(AbstractOperator):
    """
    Operator which splits a shape into strips or squares along a give directional angle

    Attributes:
        num_output_tags: int
            number of outputs tags this operator will produce
        parameters: list[OperatorParameter]
            list of parameters that define the operator

    """

    num_output_tags: int = 1
    parameters = [
        OperatorParameter(name="width", data_type=ParameterDataType.FLOAT, default=0.1,
                          description="width of the split"),
        OperatorParameter(name="angle", data_type=ParameterDataType.FLOAT, default=0.0,
                          description="angle of the split lines in radians (-PI to PI)"),
        OperatorParameter(name="cross_split", data_type=ParameterDataType.BOOL, default=False,
                          description="if the split should be split along both x and y axis"),
    ]

    def execute(self, shapes: list, output_tags: list) -> list:
        self.output_tags = output_tags
        for shape in shapes:
            self.split_shape(shape)

        return self.new_shapes

    def split_shape(self, shape) -> list:
        """
        will take a shape and bisect it via parralel strips

        todo: implement angle and cross parameters
        """
        x = 0
        y = 0
        width = self.get_parameter_value("width")
        # loop through x and y
        while x < 1 and y < 1:
            y += width

            # create the strip to divide the shape by
            strip = Polygon([(x, y), (1, y), (1, y + width), (x, y + width)])
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
                    #else:
                        # todo: might be some other types of geometry we need to handle


            if(new_polys):
                multi = MultiPolygon(new_polys)
                new_shape = Shape(geometry=multi, group_id=0, shape_id=len(self.new_shapes))
                new_shape.parent_shape = shape
                new_shape.tag = self.output_tags[0]
                self.new_shapes.append(new_shape)
        return
