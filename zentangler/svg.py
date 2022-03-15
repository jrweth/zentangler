import svgwrite
from svgwrite import Drawing
from svgwrite.path import Path
from shape import Shape
from polygon import Polygon

class SVG:
    def __init__(self, filename: str):
        self.dwg = Drawing(filename, profile='tiny')
        self.dwg.viewbox(0, 0, 1, 1)

    def add_shape(self, shape: Shape):
        """
        function to add a shape path to the svg
        """
        pathStr = self.get_polygon_path(shape.outer_polygon)
        for i in range(0, len(shape.inner_polygons)):
            p = shape.inner_polygons[i]
            pathStr += ' ' + self.get_polygon_path(p)
        path = svgwrite.path.Path(d=pathStr, stroke="black", fill="blue", stroke_width=0.01, fill_rule="evenodd" )
        self.dwg.add(path)

    def get_polygon_path(self, polygon: Polygon) -> str:
        points = polygon.points
        pathStr = 'M ' + str(points[0][0]) + ' ' + str(points[0][1])
        for i in range(1, len(points)):
            pathStr += ' L ' + str(points[i][0]) + ' ' + str(points[i][1])
        pathStr += 'z'
        return pathStr

    def save_svg(self):
        self.dwg.save()