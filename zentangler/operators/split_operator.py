import math
from perlin_noise import PerlinNoise
from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.operator_parameter import OperatorParameter, ParameterDataType, OperatorParameterValue
from zentangler.shape import Shape
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely import affinity


def sineCurveLine(numPoints):
    """
    return the points of a sine curve between 0 and 1
    """
    points = []
    for i in range(numPoints+1):
        x = i/numPoints
        points.append((x, math.sin(i * math.pi * 2 / numPoints)))
    return points


def halfCircleLine(numPoints):
    """
    return the points of a half circle between 0 and 1
    """
    points = []
    for i in range(numPoints+1):
        x = i/numPoints
        y = math.sqrt(0.25 - math.pow((x - 0.5), 2))
        points.append((x, y))
    return points


def noiseLine(numPoints):
    points = []
    for i in range(numPoints+1):
        x = i/numPoints
        y = 0
        points.append((x, y))
    return points


def getPerlinJitter(x, y, seed):
    noise1 = PerlinNoise(octaves=1, seed=seed)
    noise2 = PerlinNoise(octaves=2, seed=seed)
    noise3 = PerlinNoise(octaves=4, seed=seed)
    jitter = noise1([x, y])
    jitter += 0.5 * noise2([x, y])
    jitter += 0.25 * noise3([x, y])
    return jitter


# lines defined by a series of points going from x=0 to x=1
LINE_STYLE = {
    "STRAIGHT": [(0, 0), (1, 0)],
    "JAGGED": [(0, 0), (0.25, 0.25), (0.75, -0.25), (1, 0)],
    "STEPPED": [(0, 0), (0.25, 0), (0.25, .5), (0.75, .5), (.75, 0), (1, 0)],
    "CURVED": sineCurveLine(20),
    "HALF_CIRCLE": halfCircleLine(20),
    "NOISE": noiseLine(20)
}


class SplitOperator(AbstractOperator):
    """
    Operator which splits a shape into strips or squares along a give directional angle

    Attributes:
        num_output_tags: int
            number of outputs tags this operators will produce
        parameters: list[OperatorParameter]
            list of parameters that define the operators

    """

    num_output_tags: int = 1
    parameters = [
        OperatorParameter(name="width", data_type=ParameterDataType.FLOAT, default=0.1,
                          description="width of the split", range_start=0.005, range_end=0.8),
        OperatorParameter(name="angle", data_type=ParameterDataType.FLOAT, default=0.0,
                          description="angle of the split lines in degrees (-90 to 90)", range_start=-90t range_end=90),
        OperatorParameter(name="cross_split", data_type=ParameterDataType.BOOL, default=False,
                          description="if the split should be split along both x and y axis"),
        OperatorParameter(name="line_style", data_type=ParameterDataType.STRING, default="STRAIGHT",
                          options=["STRAIGHT", "JAGGED", "STEPPED", "CURVED", "HALF_CIRCLE", "NOISE"],
                          description="the type of line style to create the splits"),
        OperatorParameter(name="line_style_scale_x", data_type=ParameterDataType.FLOAT, default=0.1,
                          description="how much the line style is scaled along the x axis", range_start=0.001, range_end=1.0),
        OperatorParameter(name="line_style_scale_y", data_type=ParameterDataType.FLOAT, default=0.1,
                          description="how much the line style is scaled along the y axis", range_start=0.001, range_end=1.0),
        OperatorParameter(name="random_seed", data_type=ParameterDataType.INT, default=1,
                          description="seed for any random elements (eg. noise line)", range_start=1, range_end=1000)
    ]

    def __init__(self, parameter_values: list):
        """
        initialize the parameters and build the basic strip for splitting
        """
        AbstractOperator.__init__(self, parameter_values)

    def execute(self, shapes: list, output_tags: list) -> list:
        self.new_shapes = []
        self.split_strip_points = self.build_polygon_strip_points()
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
            angle = self.get_parameter_value("angle")
            new_angle = angle - 90
            if new_angle < -90:
                new_angle += 180
            self.set_parameter_value(OperatorParameterValue(name="angle", value=new_angle))

            # rerun
            for shape in second_pass_shapes:
                self.split_shape(shape)

            self.set_parameter_value(OperatorParameterValue(name="angle", value=angle))

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
            strip = self.get_offset_polygon_strip(y)
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
                new_shape.stroke_width = shape.stroke_width
                new_shape.stroke_color = shape.stroke_color
                new_shape.fill_color = shape.fill_color
                self.new_shapes.append(new_shape)
        return

    def build_polygon_strip_points(self):
        """
        build the polygon points for one strip based upon line style, line style scale and width
        """
        width = self.get_parameter_value("width")
        scale_x = self.get_parameter_value("line_style_scale_x")
        scale_y = self.get_parameter_value("line_style_scale_y")
        line_style = self.get_parameter_value("line_style")
        seed = self.get_parameter_value("random_seed")
        line_points = LINE_STYLE[line_style]

        if line_style == "NOISE":
            for i in range(len(line_points)):
                x = line_points[i][0]
                y = line_points[i][1]
                line_points[i] = (x, getPerlinJitter(x, y, seed) * scale_y)

        # we start creating the line at -2 so when rotating the polygon still intersect the unit square
        start_x = -2
        end_x = 2
        current_x = start_x

        # create the bottom line
        poly_strip_points = []
        poly_strip_points.append((current_x, 0))
        while current_x <= end_x:
            for i in range(1, len(line_points)):
                x = current_x + line_points[i][0] * scale_x
                y = line_points[i][1] * scale_y
                poly_strip_points.append((x, y))
            current_x += scale_x

        # cycle backwards through the points but add the width for the top line
        current_x -= scale_x
        while current_x >= start_x:
            for i in reversed(range(1, len(line_points))):
                x = current_x + line_points[i][0] * scale_x
                y = line_points[i][1] * scale_y + width
                poly_strip_points.append((x, y))
            current_x -= scale_x

        #add the last point
        current_x += scale_x
        poly_strip_points.append((current_x, 0 + width))

        return poly_strip_points

    def get_offset_polygon_strip(self, y_offset):
        """
        creates a polygon based upon our split strip points but offset by the width
        """
        offsetPoints = []
        for point in self.split_strip_points:
            x = point[0]
            y = point[1] + y_offset
            offsetPoints.append((x, y))
        return Polygon(offsetPoints)

