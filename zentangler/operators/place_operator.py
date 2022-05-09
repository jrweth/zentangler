import random
import copy
import math
from shapely.geometry import MultiPolygon, Polygon, Point
from shapely.affinity import translate, scale, rotate
from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.operator_parameter import OperatorParameter, ParameterDataType, OperatorParameterValue
from zentangler.shape import Shape
from zentangler.svg import SVG


def ngon_points(num_points):
    """
    Get the points of a circle
    """
    points = []
    for i in range(num_points):
        x = math.cos(math.radians(i * 360 / num_points)) / 2
        y = math.sin(math.radians(i * 360 / num_points)) / 2
        points.append((x, y))
    return points


def nstar_points(num_points, inner_radius):
    """
    Get the points of a star with n points and inner radius
    """
    points = []
    for i in range(num_points):
        x = math.cos(math.radians(i * 360 / num_points)) / 2
        y = math.sin(math.radians(i * 360 / num_points)) / 2
        points.append((x, y))
        x = inner_radius * math.cos(math.radians((i + 0.5) * 360 / num_points))
        y = inner_radius * math.sin(math.radians((i + 0.5) * 360 / num_points))
        points.append((x, y))
    return points


SHAPE_TYPES = {
    "SQUARE": [(-0.5, 0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)],
    "CIRCLE": ngon_points(36),
    "STAR": nstar_points(5, .15)
}


class PlacementGrid():
    def __init__(self, orig_poly: MultiPolygon, operator):
        self.orig_poly = orig_poly
        self.operator = operator
        self.min_distance = operator.get_parameter_value("min_distance")
        self.min_size = operator.get_parameter_value("min_size")
        self.max_size = operator.get_parameter_value("max_size")
        self.random_seed = operator.get_parameter_value("random_seed")
        self.placement_type = operator.get_parameter_value("placement_type")
        self.grid_voxel_size = max(self.min_size, self.min_distance)
        # if we have a grid max the voxel size slightly larger
        if self.placement_type == "grid":
            self.grid_voxel_size = max(self.min_size, self.min_distance) * 1.00001
        # else make the voxel size half the size
        else:
            self.grid_voxel_size = self.grid_voxel_size / 2
        # set a hard limit for voxel size
        if(self.grid_voxel_size < 0.005):
            self.grid_voxel_size = 0.005
        bounds = orig_poly.bounds
        self.grid_start_x = bounds[0]
        self.grid_start_y = bounds[1]
        self.grid_dim_x = math.ceil((bounds[2] - bounds[0]) / self.grid_voxel_size)
        self.grid_dim_y = math.ceil((bounds[3] - bounds[1]) / self.grid_voxel_size)
        self.init_grid()

    def init_grid(self):
        """
        Create a grid with each voxel being the size of the min distance and totally covering the original shape
        """
        bounds = self.orig_poly.bounds
        x = bounds[0]
        self.voxels_available = []
        self.voxel_to_index = {}

        x_index = 0
        d = self.grid_voxel_size
        # get the set of voxels that lie in the space
        while x < bounds[2]:
            y_index = 0
            y = bounds[1]
            while y < bounds[3]:
                voxel = Polygon([(x, y), (x + d, y), (x + d, y + d), (x, y + d)]);
                if voxel.difference(self.orig_poly).is_empty:
                    self.add_voxel((x_index, y_index))
                y_index += 1
                y += d
            x += d
            x_index += 1

        num_voxels = len(self.voxels_available) + 1
        self.num_iterations = math.ceil(5000 / num_voxels)
        if self.num_iterations > 100:
            self.num_iterations = 100


    def add_voxel(self, voxel):
        if voxel in self.voxel_to_index:
            return
        self.voxels_available.append(voxel)
        self.voxel_to_index[voxel] = len(self.voxels_available)-1

    def remove_voxel(self, voxel):
        position = self.voxel_to_index.pop(voxel)
        last_item = self.voxels_available.pop()
        if position != len(self.voxels_available):
            self.voxels_available[position] = last_item
            self.voxel_to_index[last_item] = position

    def get_next_position_and_size(self):
        iterations = 0
        intersecting_voxels_empty = False
        while iterations < self.num_iterations and not intersecting_voxels_empty:
            iterations += 1
            voxel = random.choice(self.voxels_available)
            voxel_start_x = self.grid_start_x + voxel[0] * self.grid_voxel_size
            voxel_start_y = self.grid_start_y + voxel[1] * self.grid_voxel_size
            if self.placement_type == "grid":
                x = voxel_start_x + self.grid_voxel_size / 2
                y = voxel_start_y + self.grid_voxel_size / 2
            else:
                x = voxel_start_x + random.uniform(0, 1) * self.grid_voxel_size
                y = voxel_start_y + random.uniform(0, 1) * self.grid_voxel_size
            size = random.uniform(self.min_size, self.max_size)

            intersecting_voxels_empty = True
            intersecting = self.get_intersecting_voxels((x,y), size, None)
            for v in intersecting:
                # if we have an intersecting voxel, shrink the size, move toward center and try again
                if v not in self.voxel_to_index.keys():
                    intersecting_voxels_empty = False
                    break

        if intersecting_voxels_empty:
            for v in intersecting:
                self.remove_voxel(v)
            return ((x, y), size)
        else:
            self.remove_voxel(voxel)
            return None



    def get_positions_and_sizes(self):
        pos_and_sizes = []
        while len(self.voxels_available) > 0:
            pos_and_size = self.get_next_position_and_size()
            if pos_and_size is not None:
                pos_and_sizes.append(pos_and_size)
        return pos_and_sizes

    def get_intersecting_voxels(self, center_point, size, new_poly):
        # get the start and end voxel index for x axis
        start_x = center_point[0] - (size / 2)
        start_voxel_x = math.floor((start_x - self.grid_start_x) / self.grid_voxel_size)
        end_x = center_point[0] + (size / 2)
        end_voxel_x = math.floor((end_x - self.grid_start_x) / self.grid_voxel_size)

        #get the start and end voxel index for y axis
        start_y = center_point[1] - (size / 2)
        start_voxel_y = math.floor((start_y - self.grid_start_y) / self.grid_voxel_size)
        end_y = center_point[1] + (size / 2)
        end_voxel_y = math.floor((end_y - self.grid_start_y) / self.grid_voxel_size)

        intersecting_voxels = []
        for x_index in range(start_voxel_x, end_voxel_x + 1):
            for y_index in range(start_voxel_y, end_voxel_y + 1):
                intersecting_voxels.append((x_index, y_index))

        return intersecting_voxels


class PlaceOperator(AbstractOperator):
    """
    operator to shapes within other shapes
    """

    num_output_tags = 2

    parameters = [
        OperatorParameter(name="shape_type", data_type=ParameterDataType.STRING, default='circle',
                          description="the type of shape to place",
                          options=['circle', 'ngon', 'star'],
                          is_multiple=False
                          ),
        OperatorParameter(name="num_shape_sides", data_type=ParameterDataType.INT, default=6,
                          description="the number of sides for the ngon",
                          range_start=3, range_end=24,
                          is_multiple=False
                          ),
        OperatorParameter(name="placement_type", data_type=ParameterDataType.STRING, default='random',
                          description="way to place shape(s)",
                          options=['random', 'grid'],
                          is_multiple=False
                          ),
        OperatorParameter(name="min_size",
                          data_type=ParameterDataType.FLOAT,
                          default=0.1,
                          description="the minimum size that the shape can be",
                          range_start=0.01, range_end=0.5
                          ),
        OperatorParameter(name="max_size",
                          data_type=ParameterDataType.FLOAT,
                          default=0.1,
                          description="the maximum size that the shape can be",
                          range_start=0.005, range_end=0.5
                          ),
        OperatorParameter(name="min_distance",
                          data_type=ParameterDataType.FLOAT,
                          default=0.1,
                          description="the minimum distance between shapes",
                          range_start=0.01, range_end=1.0
                          ),
        OperatorParameter(name="rotation",
                          data_type=ParameterDataType.INT,
                          default=1,
                          description="the rotation of the shape",
                          range_start=0,
                          range_end=359
                          ),
        OperatorParameter(name="rotation_random",
                          data_type=ParameterDataType.BOOL,
                          default=False,
                          description="if the rotation of the shapes should be random",
                          ),
        OperatorParameter(name="random_seed", data_type=ParameterDataType.INT, default=1,
                          description="seed for any random elements (e.g. rotation, shape placement)",
                          range_start=1, range_end=1000),
        OperatorParameter(name="optimized",
                          data_type=ParameterDataType.BOOL,
                          default=True,
                          description="flag to speed up shape placement, results are less dense but speedier",
                          ),
    ]

    def __init__(self, parameterValues):
        AbstractOperator.__init__(self, parameterValues)

    def execute(self, shapes: list, output_tags: list) -> list:
        random.seed(self.get_parameter_value("random_seed"))
        self.new_shapes = []
        self.base_polygon: Polygon = self.get_base_polygon()

        random.seed(self.get_parameter_value("random_seed"))
        shape_id = 0
        remainder_shape_id = 0
        optimized = self.get_parameter_value("optimized")

        for i in range(len(shapes)):
            orig_geometry: MultiPolygon = shapes[i].geometry
            if optimized:
                new_polygons: [Polygon] = self.get_new_polygons_optimized(orig_geometry)
            else:
                new_polygons: [Polygon] = self.get_new_polygons(orig_geometry)

            for new_polygon in new_polygons:
                orig_geometry = orig_geometry.difference(new_polygon)
                new_shape = shapes[i].clone()
                new_shape.geometry = MultiPolygon([new_polygon])
                new_shape.parent_shape = shapes[i]
                new_shape.tag = output_tags[0]
                new_shape.shape_id = shape_id
                shape_id += 1
                self.new_shapes.append(new_shape)

            new_shape = shapes[i].clone()
            new_shape.parent_shape = shapes[i]
            new_shape.tag = output_tags[1]
            new_shape.gid = 0
            new_shape.shape_id = remainder_shape_id
            new_shape.geometry = AbstractOperator.convert_to_multipolygon(orig_geometry)
            remainder_shape_id += 1

            self.new_shapes.append(new_shape)

        return self.new_shapes

    def get_new_polygons_optimized(self, orig_geometry: MultiPolygon):
        new_polygons = []
        min_size = self.get_parameter_value("min_size")
        max_size = self.get_parameter_value("max_size")
        min_distance = self.get_parameter_value("min_distance")
        random_seed = self.get_parameter_value("random_seed")

        grid = PlacementGrid(orig_geometry, self)
        # create the set of voxels that
        position_and_sizes = grid.get_positions_and_sizes()
        new_polygons = []
        for ps in position_and_sizes:
            size = ps[1]
            x = ps[0][0]
            y = ps[0][1]
            scaled = scale(self.base_shape, xfact=size, yfact=size, origin=(0, 0))
            rotated = self.rotate_polygon(scaled)
            poly = translate(rotated, x, y, 0)
            new_polygons.append(poly)


        return new_polygons

    def get_new_polygons(self, orig_geometry):
        center_points = self.generate_center_points(orig_geometry)

        new_polygons = []
        space_unavailable = Polygon([(-100, -100), (-100, -101), (-101, -101)])
        for center in center_points:
            center_point = Point(center[0], center[1])

            # check to make sure that our center point isn't already in the unavailable space
            center_intersect = space_unavailable.intersection(center_point)
            if center_intersect.is_empty:
                polygon, space_unavailable = self.get_polygon_at_location(center_point, orig_geometry, space_unavailable)
                if polygon is not None:
                    new_polygons.append(polygon)

        return new_polygons

    def generate_center_points(self, orig_geometry):
        placement_type = self.get_parameter_value("placement_type")
        if placement_type == "grid":
            return self.generate_grid_center_points(orig_geometry)
        return self.generate_random_center_points(orig_geometry)

    def generate_random_center_points(self, orig_geometry):
        random.seed(self.get_parameter_value("random_seed"))
        bounds = orig_geometry.bounds
        min_x = bounds[0]
        min_y = bounds[1]
        max_x = bounds[2]
        max_y = bounds[3]
        min_size = self.get_parameter_value("min_size")
        min_distance = self.get_parameter_value("min_distance")
        grid_size = max(min_distance, min_size)

        x_size = max_x - min_x
        y_size = max_y - min_y
        num_points = 5 * math.ceil((x_size * y_size) / (grid_size * grid_size))

        center_points = set()
        for i in range(num_points):
            point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
            if orig_geometry.contains(point):
                center_points.add((point.x, point.y))
        return center_points

    def generate_grid_center_points(self, orig_geometry):
        center_points = set()
        bounds = orig_geometry.bounds
        min_x = bounds[0]
        min_y = bounds[1]
        max_x = bounds[2]
        max_y = bounds[3]
        min_dist = self.get_parameter_value("min_distance")
        min_size = self.get_parameter_value("min_size")
        grid_size = max(min_dist, min_size)

        x = min_x
        while x < max_x:
            y = min_y + grid_size / 2
            while y < max_y:
                point = Point(x, y)
                if orig_geometry.contains(point):
                    center_points.add((x, y))
                y += grid_size
            x += grid_size
        return center_points

    def get_polygon_at_location(self, p: Point, orig_geometry, space_unavailable):
        """
        get the shape at the specified location
        """
        min_distance = self.get_parameter_value("min_distance")
        min_size = self.get_parameter_value("min_size")
        max_size = self.get_parameter_value("max_size")
        scale_by = random.uniform(min_size, max_size)

        # loop and try to fit until we've scaled below the minimum size
        while scale_by >= min_size:
            scaled = scale(self.base_shape, xfact=scale_by, yfact=scale_by, origin=(0,0))
            rotated = self.rotate_polygon(scaled)
            poly = translate(rotated, p.x, p.y, 0)
            outside = poly.difference(orig_geometry)
            in_unavailable_space = poly.intersection(space_unavailable)

            # if there is no part of our shape poking outside or intersecting with unavailable space
            if outside.is_empty and in_unavailable_space.is_empty:
                # if the size is bigger than min_distance then add the poly
                if (scale_by > min_distance):
                    space_unavailable = space_unavailable.union(poly)
                else:
                    space_holder = Polygon(ngon_points(6))
                    space_holder = scale(space_holder, xfact=min_distance, yfact=min_distance, origin=(0,0))
                    space_holder = translate(space_holder, p.x, p.y, 0)
                    space_unavailable = space_unavailable.union(space_holder)
                return poly, space_unavailable
            # try to scale down to fit for next iteration
            scale_by = scale_by * 0.75

        return None, space_unavailable

    def rotate_polygon(self, polygon: Polygon):
        angle = self.get_parameter_value("rotation")
        if self.get_parameter_value("rotation_random"):
            angle = random.uniform(0, 359)

        return rotate(polygon, angle)

    def get_base_polygon(self):
        """
        get the base shape to place
        return: Polygon
        """
        num_shape_sides = self.get_parameter_value("num_shape_sides")
        shape_type = self.get_parameter_value("shape_type")
        if shape_type == 'circle':
            self.base_shape = Polygon(ngon_points(72))
        elif shape_type == 'star':
            self.base_shape = Polygon(nstar_points(num_shape_sides, .15))
        elif shape_type == 'ngon':
            self.base_shape = Polygon(ngon_points(num_shape_sides))

    def create_thumbnail(self, png_filename: str):
        min_size = self.get_parameter_value("min_size")
        min_distance = self.get_parameter_value("min_distance")
        grid_size = max(min_size, min_distance)
        num_shapes = (1/grid_size)*(1/grid_size)


        if num_shapes > 8000:

            points = [(0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4)]
            outer_points = [(0, 0), (0, 1), (1, 1), (1, 0)]
            m_poly = MultiPolygon([Polygon(points)])
            shapes = [Shape(geometry=m_poly, shape_id=0)]
            new_shapes = self.execute(shapes, ["shapes", "remainder"])
            # create the svg and png files
            svg = SVG(png_filename.replace(".png", ".svg"))
            svg.add_shape(Shape(geometry=MultiPolygon([Polygon(outer_points)])))
            for shape in new_shapes:
                svg.add_shape(shape)
            svg.save_png(png_filename, resolution=100)
        else:
            return AbstractOperator.create_thumbnail(self, png_filename)

