import svgwrite
from svgwrite import Drawing
from svgwrite.path import Path
from shape import Shape
from polygon import Polygon

class SVG:
    """
    Class for converting polygon instances into SVG drawings
    """
    def __init__(self, filename: str):
        self.dwg = Drawing(filename, profile='tiny')
        self.dwg.viewbox(0, 0, 1, 1)

    def add_shape(self, shape: Shape):
        """
        function to add a zentangle shape to the svg
        """

        # add the outer polygon to the path
        pathStr = self.get_polygon_path(shape.outer_polygon)

        #loop through the inner polygon "holes" and add geometry to the path
        for i in range(0, len(shape.inner_polygons)):
            p = shape.inner_polygons[i]
            pathStr += ' ' + self.get_polygon_path(p)
        path = svgwrite.path.Path(d=pathStr, stroke="black", fill="blue", stroke_width=0.01, fill_rule="evenodd" )
        self.dwg.add(path)

    def get_polygon_path(self, polygon: Polygon) -> str:
        """
        given a polygon, create the svg path that defines it
        """
        points = polygon.points
        pathStr = 'M ' + str(points[0].x) + ' ' + str(points[0].y)
        for i in range(1, len(points)):
            pathStr += ' L ' + str(points[i].x) + ' ' + str(points[i].y)
        pathStr += 'z'
        return pathStr

    def save_svg(self):
        self.dwg.save()