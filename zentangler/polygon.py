from point import Point
from utils import do_intersect


class Polygon:
    """
    A class that contains a list of 2D points that define a polygon
    Shapes are assumed to have a clockwise ordering of points unless they are defining the "holes" within
    another polygon in which case they will be ordered counter-clockwise
    """
    def __init__(self, points:  list = []):
        self.points = points

    def get_intersection_indexes(self, start_point: Point, end_point: Point) -> list:
        """
        returns the indexes of the polygon points which start a line segment
        which intersects with the provided line segment

        Parameters
        ----------
        start_point: Point
            the start paint of the line segment to test for intersections
        end_point: Point
            the end paint of the line segment to test for intersections
        """
        intersections = []
        for i in range(len(self.points)):
            poly_point_1 = self.points[i]
            poly_point_2 = self.points[(i+1) % len(self.points)]
            if(do_intersect(start_point, end_point, poly_point_1, poly_point_2)):
                intersections.append(i)
        return intersections










