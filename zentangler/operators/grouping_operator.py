import random
from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.svg import SVG
from zentangler.operators.operator_parameter import OperatorParameter, ParameterDataType, OperatorParameterValue


def get_sample_group_color(group_id: int):
    random.seed(group_id)
    return (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0,1))


class UngroupOperator(AbstractOperator):

    num_output_tags = 1

    def execute(self, shapes: list, output_tags: list) -> list:
        gid = 0

        for shape in shapes:
            shape.group_id = gid
            shape.tag = shape.tag

            self.new_shapes.append(shape)
            gid += 1

        return self.new_shapes

    def create_thumbnail(self, png_filename: str):
        shapes = self.get_thumbnail_shapes_grid(0.25)

        output_tags = []
        new_shapes = self.execute(shapes, output_tags)

        #create the svg and png files
        svg = SVG(png_filename.replace(".png", ".svg"))
        for shape in new_shapes:
            shape.fill_color = get_sample_group_color(shape.group_id)
            svg.add_shape(shape)
        svg.save_png(png_filename, resolution=100)

class RegroupOperator(AbstractOperator):

    parameters = [
        OperatorParameter(name="k", data_type=ParameterDataType.INT, default=2,
                          description="number of groups", range_start=2, range_end=10),
    ]
    num_output_tags = 0

    def execute(self, shapes: list, output_tags: list) -> list:
        k = self.get_parameter_value("k")

        for shape in shapes:
            shape.group_id = shape.shape_id % k
            self.new_shapes.append(shape)

        return self.new_shapes

    def create_thumbnail(self, png_filename: str):
        shapes = self.get_thumbnail_shapes_grid(0.25)

        output_tags = []
        new_shapes = self.execute(shapes, output_tags)

        #create the svg and png files
        svg = SVG(png_filename.replace(".png", ".svg"))
        for shape in new_shapes:
            shape.fill_color = get_sample_group_color(shape.group_id)
            svg.add_shape(shape)
        svg.save_png(png_filename, resolution=100)

