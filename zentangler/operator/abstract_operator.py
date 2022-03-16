from abc import ABC, abstractmethod
from zentangler.shape import Shape
class AbstractOperator(ABC):

    @abstractmethod
    def execute(self, shapes: list, output_tags) -> list:
        pass