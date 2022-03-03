from abc import ABC, abstractmethod
class AbstractOperator(ABC):

    @abstractmethod
    def execute(self, tangle):
        pass