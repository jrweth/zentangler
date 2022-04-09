import svgwrite
from svgwrite import Drawing
from svgwrite.path import Path
from zentangler.shape import Shape
import cairosvg

class SVG:
    """
    Class for converting polygon instances into SVG drawings
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.dwg = Drawing(filename, profile='tiny')
        self.dwg.viewbox(0, 0, 1, 1)

    def add_shape(self, shape: Shape):
        """
        function to add a zentangle shape to the svg
        """
        # add the outer polygon to the path
        for poly in shape.geometry.geoms:
            pathStr = self.get_polygon_path(poly.exterior.coords)

            #loop through the inner polygon "holes" and add geometry to the path
            for i in range(0, len(poly.interiors)):
                points = poly.interiors[i].coords
                pathStr += ' ' + self.get_polygon_path(points)
            path = svgwrite.path.Path(d=pathStr, stroke=shape.stroke_color, fill=shape.fill_color, stroke_width=shape.stroke_width, fill_rule="evenodd" )
            self.dwg.add(path)

    def get_polygon_path(self, points: list) -> str:
        """
        given a list of points, create the svg path that defines it
        """
        pathStr = 'M ' + str(points[0][0]) + ' ' + str(1.0 - points[0][1])
        for i in range(1, len(points)):
            pathStr += ' L ' + str(points[i][0]) + ' ' + str(1.0 - points[i][1])
        pathStr += 'z'
        return pathStr

    def save_svg(self):
        self.dwg.save()

    def save_png(self, png_filename, resolution: int = 1024):
        self.save_svg()
        cairosvg.svg2png(url=self.filename, write_to=png_filename, scale=resolution)
