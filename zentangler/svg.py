import os.path
import svgwrite
import platform
from math import floor
from svgwrite import Drawing
from svgwrite.path import Path
from zentangler.shape import Shape
from zentangler.config_manager import ConfigManager
import subprocess

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
            path = svgwrite.path.Path(d=pathStr,
                                      stroke=self.get_rgb_string(shape.stroke_color),
                                      fill=self.get_rgb_string(shape.fill_color),
                                      stroke_width=shape.stroke_width,
                                      fill_rule="evenodd")
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

    def get_rgb_string(self, rgb: ()):
        """
        given a set of rgb with values (0-1, 0-1, 0-1) return the rgb(0-255, 0-255, 0-255) string
        """
        return "rgb(" + str(floor(rgb[0] * 255)) \
               + ", " + str(floor(rgb[1] * 255)) \
               + ", " + str(floor(rgb[2] * 255)) + ")"

    def save_svg(self):
        self.dwg.save()

    def save_png(self, png_filename, resolution: int = 1024):
        self.save_svg()

        # get the inkscape executable from the config manager
        if not ConfigManager.config_loaded:
            ConfigManager.load_config_file()
        inkscape_path = ConfigManager.inkscape_executable

        if inkscape_path is None or not os.path.exists(inkscape_path):
            print("Inkscape path is not set in Zentangler configuration")
        else:
            if platform.system() == 'Windows':
                cmd = ' '.join((
                            inkscape_path,
                            self.filename,
                            "--export-width=" + str(resolution),
                            "--export-height=" + str(resolution),
                            "--export-type=\"png\"",
                            "--export-filename=" + png_filename))
                sb  = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                (output, err) = sb.communicate()
                exit_code = sb.wait()
                if not exit_code == 1:
                    print(err)
            else:
                args = [
                    inkscape_path,
                    self.filename,
                    "--export-area-page",
                    "-w", str(resolution),
                    "-h", str(resolution),
                    "--export-png=" + png_filename
                ]
                subprocess.run(args)


