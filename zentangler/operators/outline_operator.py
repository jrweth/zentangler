import pyclipper
import copy

from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.operator_parameter import OperatorParameter, ParameterDataType, OperatorParameterValue
from zentangler.shape import Shape
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection

class OutlineOperator(AbstractOperator):
    """
    Operator which splits a shape into strips or squares along a give directional angle

    Attributes:
        num_output_tags: int
            number of outputs tags this operators will produce
        parameters: list[OperatorParameter]
            list of parameters that define the operators

    """


    precision = 1000000
    """
    to use clipper we need to convert from floats (0-1) to ints. The higher this number is the more precision we have)
    """
    num_output_tags: int = 2
    parameters = [
        OperatorParameter(name="width", data_type=ParameterDataType.FLOAT, default=0.1,
                          description="width of the split", range_start=0.001, range_end=1.0),
    ]

    def execute(self, shapes: list, output_tags: list) -> list:
        self.output_tags = output_tags
        self.tag1_shape_id = 0
        self.tag2_shape_id = 0

        # loop through the shapes provided and do the split
        self.new_shapes = []
        for shape in shapes:
            self.outline_shape(shape)

        return self.new_shapes

    def outline_shape(self, shape: Shape) -> list:
        """
        will take a shape and create outlines of shape and holes and any remainder

        Parameters:
            shape: Shape
                The shape to create the outline for

        return: list[Shape]
        """
        for polygon in shape.geometry.geoms:

            try:

                # set up the clipper offsetter
                offsetter = pyclipper.PyclipperOffset()
                exterior = OutlineOperator.polygon_float_pts_to_int(polygon.exterior.coords)

                #make sure exterior is clockwise
                if not OutlineOperator.polygon_is_clockwise(exterior):
                    exterior.reverse()

                # add the exterior polygon to our offsetter
                offsetter.AddPath(exterior, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)

                for interior in polygon.interiors:
                    interiorPoints = OutlineOperator.polygon_float_pts_to_int(interior.coords)

                    # make sure interior polygons are counter-clockwise
                    if OutlineOperator.polygon_is_clockwise(interiorPoints):
                        interiorPoints.reverse()

                    # add interior shapes to our offsetter
                    offsetter.AddPath(interiorPoints, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)

                #get the solution which returns the new offset borders
                solution = offsetter.Execute(-self.get_parameter_value("width") * OutlineOperator.precision)

                # get the exterior polygon and make the new hole the outermost outline (solution 0)
                outline1 = Polygon(polygon.exterior.coords, [OutlineOperator.polygon_int_pts_to_float(solution[0])])
                #remove all the original holes as well in case they end up in our border
                for orig_hole in polygon.interiors:
                    outline1 = outline1.difference(Polygon(orig_hole))

                # create the outer outline shape
                outerShape: Shape = copy.deepcopy(shape)
                outerShape.tag = self.output_tags[0]
                outerShape.geometry = MultiPolygon([outline1])
                outerShape.group_id = 0
                outerShape.shape_id = self.tag1_shape_id
                self.tag1_shape_id = self.tag1_shape_id + 1
                self.new_shapes.append(outerShape)

                #get the interior polygon (solution[0]) and make the remainder shape
                remainder_shape: Shape = shape.clone()
                remainder_shape.tag = self.output_tags[1]
                remainder_exterior = OutlineOperator.polygon_int_pts_to_float(solution[0])

                #get all the additional solutions as holes in the remainder
                remainder_interiors = []
                for i in range(1, len(solution)):
                    remainder_interiors.append(OutlineOperator.polygon_int_pts_to_float(solution[i]))
                remainder_polygon = Polygon(remainder_exterior, remainder_interiors)
                remainder_shape.geometry = MultiPolygon([remainder_polygon])
                remainder_shape.tag = self.output_tags[1]
                remainder_shape.group_id = 0
                remainder_shape.shape_id = self.tag2_shape_id
                self.tag2_shape_id = self.tag2_shape_id + 1
                self.new_shapes.append(remainder_shape)

                #get the internal outlines
                for interior_outline in remainder_interiors:
                    interior_outline_polygon = Polygon(interior_outline, [])
                    # remove all the original holes
                    for orig_hole in polygon.interiors:
                        interior_outline_polygon = interior_outline_polygon.difference(Polygon(orig_hole))
                    interior_outline_shape = copy.deepcopy(shape)
                    interior_outline_shape.geometry = MultiPolygon([interior_outline_polygon])
                    interior_outline_shape.tag = self.output_tags[0]
                    interior_outline_shape.group_id = 0
                    interior_outline_shape.shape_id = self.tag1_shape_id
                    self.tag1_shape_id = self.tag1_shape_id + 1
                    self.new_shapes.append(interior_outline_shape)

            except Exception as error:
                print ("error in getting outline", error)
                remainder_shape: Shape = shape.clone()
                remainder_shape.tag = self.output_tags[1]
                remainder_shape.parent_shape = shape
                self.new_shapes.append(remainder_shape)
        return

    def polygon_is_clockwise(points):
        """
        function to determine if a polygon is clockwise by summing over the product of the edges
        (x2 -x1)(y2 + y1)
        """
        sum = 0
        for i in range(len(points)):
            pt1 = points[i]

            # handle the last point case
            if i == len(points) - 1:
                pt2 = points[0]
            else:
                pt2 = points[i+1]

            sum = sum + (pt2[0] - pt1[0]) * (pt2[1] + pt2[1])

        return sum <= 0


    def polygon_float_pts_to_int(points):
        """
        since clipper only works with integers this is necessary to translate between floats (0.0 - 1.0) and ints
        """
        newPoints = []
        for p in points:
            newPoints.append( (round(p[0] * OutlineOperator.precision), round(p[1] * OutlineOperator.precision)) )
        return newPoints

    def polygon_int_pts_to_float(points):
        """
        since clipper only works with integers this is necessary to translate between ints and floats (0.0 -1.0)
        """
        newPoints = [];
        for p in points:
            newPoints.append( (p[0] / OutlineOperator.precision, p[1] / OutlineOperator.precision))
        return newPoints

