import random
import copy
from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.operator_parameter import OperatorParameter, ParameterDataType, OperatorParameterValue

class LineWidthOperator(AbstractOperator):
    """
    operator to change the line and/or fill color of a given shape
    """

    num_output_tags = 1

    parameters = [
        OperatorParameter(name="width_or_multiplier", data_type=ParameterDataType.STRING, default="width",
                          description="choice to set the absolute width or multiply the current width",
                          is_multiple=False, options=["width", "current width multiplier"]
                          ),
        OperatorParameter(name="line_width", data_type=ParameterDataType.FLOAT, default=0.01,
                          description="the absolute width of the line scaled in the 0-1 range",
                          is_multiple=False, range_start=0.001, range_end=0.5
                          ),
        OperatorParameter(name="current_width_multiplier", data_type=ParameterDataType.FLOAT, default=1.0,
                          description="the color(s) to fill the shape with",
                          is_multiple=False, range_start=0.1, range_end=10
                          ),
    ]

    def execute(self, shapes: list, output_tags: list) -> list:
        self.new_shapes = []
        shape_id = 0

        for i in range(len(shapes)):
            new_shape = copy.copy(shapes[i])
            new_shape.parent_shape = shapes[i]
            new_shape.tag = output_tags[0]
            new_shape.gid = 0
            new_shape.shape_id = shape_id
            shape_id += 1

            width_or_multiplier = self.get_parameter_value("width_or_multiplier")
            if(width_or_multiplier == "width"):
                new_shape.stroke_width = self.get_parameter_value("line_width")
            elif(width_or_multiplier == "current_width_multiplier"):
                width_multiplier = self.get_parameter_value("current_width_multiplier")
                new_shape.stroke_width = new_shape.stroke_width * self.get_parameter_value("current_width_multiplier")

            self.new_shapes.append(new_shape)

        return self.new_shapes

    def create_thumbnail(self, png_filename: str):
        return self.create_thumbnail_grid(png_filename)
