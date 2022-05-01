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
        self.new_shapes = []

        for shape in shapes:
            new_shape = shape.clone()
            new_shape.group_id = gid
            new_shape.parent_shape = shape

            self.new_shapes.append(new_shape)
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
        # OperatorParameter(name="k", data_type=ParameterDataType.INT, default=2,
        #                   description="number of groups", range_start=2, range_end=10),
        OperatorParameter(name="output_tags", data_type=ParameterDataType.LIST, default=["tag1"],
                          description="tags for grouping"),
    ]
    num_output_tags = 0

    def execute(self, shapes: list, output_tags: list) -> list:
        self.new_shapes = []

        # k = self.get_parameter_value("k")
        k = len(self.get_parameter_value("output_tags"))

        output_tags = self.get_parameter_value("output_tags")

        for shape in shapes:
            new_shape = shape.clone()
            new_shape.group_id = shape.shape_id % k
            new_shape.tag = output_tags[shape.shape_id % k]
            new_shape.parent = shape
            self.new_shapes.append(new_shape)

        return self.new_shapes

    def create_thumbnail(self, png_filename: str):
        shapes = self.get_thumbnail_shapes_grid(0.25)

        new_shapes = self.execute(shapes, self.get_parameter_value("output_tags"))

        #create the svg and png files
        svg = SVG(png_filename.replace(".png", ".svg"))
        for shape in new_shapes:
            shape.fill_color = get_sample_group_color(shape.group_id)
            svg.add_shape(shape)
        svg.save_png(png_filename, resolution=100)

