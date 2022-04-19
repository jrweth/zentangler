from abc import ABC, abstractmethod
from shapely.geometry import Polygon, MultiPolygon
from zentangler.shape import Shape
from zentangler.svg import SVG
from zentangler.operators.operator_parameter import OperatorParameter, OperatorParameterValue


class AbstractOperator(ABC):
    """
    Abstract class representing operators that can be applied to shapes

    Attributes
    ----------
        parameters: list[OperatorParameter]
            list of operators parameters required to configure this operators
    """
    parameters: list

    num_output_tags: int

    def __init__(self, parameterValues: list):
        """
        initialize the operators

        Parameters
        ----------
            parameterValues: list[ParameterValue]
                list of parameter values to instantiate the operators
        """
        self.parameterValues = parameterValues
        self.new_shapes = []

    def set_parameter_value(self, value: OperatorParameterValue):
        """
        set the parameter value
        Parameters:
            value: OperatorParameterValue
                the parameter value to set
        """
        for i in range(len(self.parameterValues)):
            if self.parameterValues[i].name == value.name:
                self.parameterValues[i] = value
                return
        self.parameterValues.append(value)

    def get_parameter_value(self, name: str):
        """
        get the parameter value by the parameter name
        """
        # loop through the provided values to retrieve the value
        for pValue in self.parameterValues:
            if pValue.name == name:
                return pValue.value

        # if no value loop through default values to return default value
        for param in self.parameters:
            if param.name == name:
                return param.default

        # return None if nothing found
        return None

    #@abstractmethod
    def execute(self, shapes: list, output_tags) -> list:
        pass

    def create_thumbnail(self, png_filename: str):
        """
        create a thumbnail at the png_filename location

        Parameters:
            png_filename: str
                filename to save the png to ending in .png
        """

        # create a square shape as our origi
        points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        m_poly = MultiPolygon([Polygon(points)])
        shape = Shape(geometry=m_poly)

        #create dummy output tags and execute
        output_tags = []
        for i in range(self.num_output_tags):
            output_tags.append("out_tag_" + str(i))
        new_shapes = self.execute([shape], output_tags)

        #create the svg and png files
        svg = SVG(png_filename.replace(".png", ".svg"))
        for shape in new_shapes:
            svg.add_shape(shape)
        svg.save_png(png_filename, resolution=100)


    def get_thumbnail_shapes_grid(self, grid_size: float =0.25):
        """
        create an grid of shapes to test the operator on
        """
        # create a square shape as our origi
        y = 0
        shapes = []
        shape_id = 0
        while y < .99:
            x = 0
            while x < .99:
                points = [(x, y), (x, y + grid_size), (x + grid_size, y + grid_size), (x + grid_size, y)]
                m_poly = MultiPolygon([Polygon(points)])
                shapes.append(Shape(geometry=m_poly, shape_id=shape_id))
                x += grid_size
                shape_id += 1
            y += grid_size
        return shapes

    def create_thumbnail_grid(self, png_filename: str):
        """
        create a thumbnail at the png_filename location

        Parameters:
            png_filename: str
                filename to save the png to ending in .png
        """
        #create dummy output tags and execute
        shapes = self.get_thumbnail_shapes_grid()
        output_tags = []
        for i in range(self.num_output_tags):
            output_tags.append("out_tag_" + str(i))
        new_shapes = self.execute(shapes, output_tags)

        #create the svg and png files
        svg = SVG(png_filename.replace(".png", ".svg"))
        for shape in new_shapes:
            svg.add_shape(shape)
        svg.save_png(png_filename, resolution=100)

    def get_parameter_definition(self, parameter_name):
        """
        get the parameter specified (not the value)

        Parameters:
            parameter_name: str
                the name of the parameter to retrieve the data type for
        """
        for param in self.parameters:
            if param.name == parameter_name:
                return param
        return None