from enum import Enum
class ParameterDataType(Enum):
    """
    parameter data type for operators
    """
    STRING = 1
    INT = 2
    FLOAT = 3
    BOOL = 4
    RGB_COLOR = 5

class OperatorParameter:
    """
    Class representing a parameter to be passed to an operators
    """

    def __init__(self,
                 name: str,
                 data_type: ParameterDataType,
                 default,
                 description: str,
                 options: list = [],
                 range_start=None,
                 range_end=None,
                 is_multiple=False
                 ):
        """
        initializer for the operators parameter

        Parameters:
            name: str
                name of the parameter to be be passed (e.g. width, height etc)
            data_type: ParameterDataType
                data type of the parameter
            default:  any
                default value for the parameter
            description: str
                description of the parameter (eg. "The width of each split segment")
            options: list
                a list of options which can be chosen from for this parameter
            range_start: int|float
                the start of the range for numeric values
            range_end: int|float
                the end of the range for numeric values

        """
        self.name = name
        self.data_type = data_type
        self.default = default
        self.description = description


class OperatorParameterValue:
    """
    class representing a named parameter value
    """
    def __init__(self, name: str, value):
        """
        initialization function
        Parameters:
            name: str
                the name of the parameter
            value:
                the value of the parameter
        """
        self.name = name
        self.value = value
