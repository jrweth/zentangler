from abc import ABC, abstractmethod
from zentangler.shape import Shape
from zentangler.operator.operator_parameter import OperatorParameter, OperatorParameterValue
class AbstractOperator(ABC):
    """
    Abstract class representing operators that can be applied to shapes

    Attributes
    ----------
        parameters: list[OperatorParameter]
            list of operator parameters required to configure this operator
    """
    parameters: list

    def __init__(self, parameterValues: list):
        """
        initialize the operator

        Parameters
        ----------
            parameterValues: list[ParameterValue]
                list of parameter values to instantiate the operator
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

    @abstractmethod
    def execute(self, shapes: list, output_tags) -> list:
        pass