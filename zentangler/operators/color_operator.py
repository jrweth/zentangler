import random
import copy
from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.operator_parameter import OperatorParameter, ParameterDataType, OperatorParameterValue

class ColorOperator(AbstractOperator):
    """
    operator to change the line and/or fill color of a given shape
    """

    num_output_tags = 1

    parameters = [
        OperatorParameter(name="line_colors", data_type=ParameterDataType.RGB_COLOR, default=[(0, 0, 0)],
                          description="the color(s) to assign to the shape lines",
                          is_multiple=True
                          ),
        OperatorParameter(name="fill_colors", data_type=ParameterDataType.RGB_COLOR, default=[(1, 1, 1)],
                          description="the color(s) to fill the shape with",
                          is_multiple=True
                          ),
        OperatorParameter(name="line_color_assignment",
                          data_type=ParameterDataType.STRING,
                          default="retain existing",
                          description="the strategy for assigning the line color",
                          options=["retain existing", "single color", "cycle colors", "random"]
                          ),
        OperatorParameter(name="fill_color_assignment",
                          data_type=ParameterDataType.STRING,
                          default="retain existing",
                          description="the strategy for assigning the fill color",
                          options=["retain existing", "single color", "cycle colors", "random"]
                          ),
        OperatorParameter(name="random_seed",
                          data_type=ParameterDataType.INT,
                          default=1,
                          description="seed for determining random color assignment",
                          ),
    ]

    def execute(self, shapes: list, output_tags: list) -> list:
        self.new_shapes = []
        random.seed(self.get_parameter_value("random_seed"))
        shape_id = 0

        for i in range(len(shapes)):
            new_shape = copy.copy(shapes[i])
            new_shape.parent_shape = shapes[i]
            new_shape.tag = output_tags[0]
            new_shape.gid = 0
            new_shape.shape_id = shape_id
            shape_id += 1

            fill_type = self.get_parameter_value("fill_color_assignment")
            fill_colors = self.get_parameter_value("fill_colors")
            if fill_type == "single color":
                new_shape.fill_color = fill_colors[0]
            elif fill_type == "cycle colors":
                new_shape.fill_color = fill_colors[i % len(fill_colors)]
            elif fill_type == "random":
                new_shape.fill_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

            line_type = self.get_parameter_value("line_color_assignment")
            line_colors = self.get_parameter_value("line_colors")
            if line_type == "single color":
                new_shape.stroke_color = line_colors[0]
            elif line_type == "cycle colors":
                new_shape.stroke_color = line_colors[i % len(line_colors)]
            elif fill_type == "random":
                new_shape.stroke_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

            self.new_shapes.append(new_shape)

        return self.new_shapes

    def create_thumbnail(self, png_filename: str):
        return self.create_thumbnail_grid(png_filename)
