from zentangler.shape import Shape
from zentangler.svg import SVG


class Expansion:
    """
    Expansion class that holds the state of tangle at a point in process of expansion
        (probably after a rule was applied)
        The shapes in a tangle at a particular expansion are the shapes in added & remainder
    """

    def __init__(self, matched: list, added: list, remainder: list): #, rule_applied):    # ??: include rule applied
        """
        initialize an expansion

        Parameters:
            matched: set of shapes matched with the rule
            added: set of new shapes added after rule is applied
            remainder: set of shaped on which rule was not applied
        """

        self.matched = []
        self.added = []
        self.remainder = []

        if matched is not None:
            self.matched = matched

        if added is not None:
            self.added = added

        if remainder is not None:
            self.remainder = remainder

        self.shapes = self.appendAllShapes()

    def appendAllShapes(self):
        self.shapes = []

        if self.matched is not None:
            for m in self.matched:
                self.shapes.append(m)

        if self.added is not None:
            for a in self.added:
                self.shapes.append(a)

        if self.remainder is not None:
            for r in self.remainder:
                self.shapes.append(r)

        return self.shapes
                
    def addToMatched(self, shape: Shape):
        self.matched.append(shape)
        self.shapes.append(shape)
        
    def addToAdded(self, shape: Shape):
        self.added.append(shape)
        self.shapes.append(shape)

    def addToRemainder(self, shape: Shape):
        self.remainder.append(shape)
        self.shapes.append(shape)

    def getShapesForNewExpansion(self):
        shapes = []

        if self.added is not None:
            for a in self.added:
                shapes.append(a)

        if self.remainder is not None:
            for r in self.remainder:
                shapes.append(r)

        return shapes

    def createExpansionSVG(self, svg_filename):
        """
        create an SVG file based upon the calculated shapes in this expansion

        Parameters:
            svg_filename: string
                the filename (path included) of the svg file to save (should end in ".svg")

        """
        svg = SVG(svg_filename)
        for shape in self.getShapesForNewExpansion():
            svg.add_shape(shape)
        svg.save_svg()

    def createExpansionPNG(self, png_filename, resolution: int = 1024):
        """
        create an PNG file based upon the calculated shapes in this expansion

        Parameters:
            png_filename: string
                the filename (path included) of the png file to save (should end in ".png")

        """
        svg_filename = png_filename.replace(".png", ".svg").replace(".PNG", ".SVG")
        svg = SVG(svg_filename)
        for shape in self.getShapesForNewExpansion():
            svg.add_shape(shape)
        svg.save_png(png_filename, resolution)


