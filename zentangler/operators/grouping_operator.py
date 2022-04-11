from zentangler.operators.abstract_operator import AbstractOperator
from zentangler.operators.operator_parameter import OperatorParameter, ParameterDataType, OperatorParameterValue


class UngroupOperator(AbstractOperator):

    num_output_tags = 1

    def execute(self, shapes: list, output_tags: list) -> list:
        gid = 0

        for shape in shapes:
            shape.group_id = gid
            shape.tag = output_tags[0]

            self.new_shapes.append(shape)
            gid += 1

        return self.new_shapes


class RegroupOperator(AbstractOperator):

    parameters = [
        OperatorParameter(name="k", data_type=ParameterDataType.INT, default=1,
                          description="number of groups"),
    ]
    num_output_tags = 0

    def execute(self, shapes: list, output_tags: list) -> list:
        k = self.get_parameter_value("k")

        for shape in shapes:
            shape.group_id = shape.shape_id % k
            shape.tag = output_tags[shape.shape_id % k]
            self.num_output_tags += 1

            self.new_shapes.append(shape)

        return self.new_shapes
