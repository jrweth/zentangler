from math import cos, sin

import shapely.geometry

from zentangler.operator.abstract_operator import AbstractOperator
from zentangler.operator.operator_parameter import OperatorParameter, ParameterDataType, OperatorParameterValue
from zentangler.shape import Shape
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely import affinity

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
                          description="angle of the split lines in degrees (-90 to 90)"),
        OperatorParameter(name="cross_split", data_type=ParameterDataType.BOOL, default=False,
                          description="if the split should be split along both x and y axis"),
    ]

    def execute(self, shapes: list, output_tags: list) -> list:
        self.output_tags = output_tags

        # loop through the shapes provided and do the split
        for shape in shapes:
            self.split_shape(shape)

        # if we are cross splitting then rerun with angle adjusted -90 degrees
        if self.get_parameter_value("cross_split"):
            # reset new shapes
            second_pass_shapes = self.new_shapes
            self.new_shapes = []

            # set the new angle
            new_angle = self.get_parameter_value("angle") - 90
            if new_angle < -90:
                new_angle += 180
            self.set_parameter_value(OperatorParameterValue(name="angle", value=new_angle))

            # rerun
            for shape in second_pass_shapes:
                self.split_shape(shape)

        return self.new_shapes

    def split_shape(self, shape) -> list:
        """
        will take a shape and bisect it via parallel horizontal strips rotated by set angle
        """

        # need to start at -1.5 so when rotating we don't go off the grid
        y = -1.5
        width = self.get_parameter_value("width")
        angle = self.get_parameter_value("angle")
        # loop through x and y
        while y < 1.5:
            y += width

            # create the strip to divide the shape by horzintal lines (use 2 for x value so when rotating we still intersect
            strip = Polygon([(-2, y), (2, y), (2, y + width), (-2, y + width)])
            # rotate the strip around the provided angle
            strip = affinity.rotate(strip, angle, (0, 0))
            new_polys = []

            # loop through each polygon in our shape and find the intersection with the strip
            for i in range(0, len(shape.geometry.geoms)):
                intersection = strip.intersection(shape.geometry.geoms[i])
                if intersection:
                    # check out what type of intersection object is returned and extract the polygons from it
                    # Add Polygons
                    if isinstance(intersection, Polygon):
                        new_polys.append(intersection)

                    # Add all polygons if MultiPolygon
                    elif isinstance(intersection, MultiPolygon):
                        for poly in intersection.geoms:
                            new_polys.append(poly)

                    # Add all polygons if GeometryCollection
                    elif isinstance(intersection, GeometryCollection):
                        for geo in intersection.geoms:
                            if isinstance(geo, Polygon):
                                new_polys.append(geo)
                    #else:
                        # todo: might be some other types of geometry we need to handle


            # if any intersection polygons found create a new multipolygon made up of new_polys and add to new_shapes
            if len(new_polys) > 0:
                multi = MultiPolygon(new_polys)
                new_shape = Shape(geometry=multi, group_id=0, shape_id=len(self.new_shapes))
                new_shape.parent_shape = shape
                new_shape.tag = self.output_tags[0]
                self.new_shapes.append(new_shape)
        return
