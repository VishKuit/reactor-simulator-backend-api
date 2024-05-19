from abc import ABC, abstractmethod

class ReactorModule(ABC):
    @abstractmethod
    def inital_calculations(self):
        pass

    @abstractmethod
    def temp_press_equations(self):
        pass

    @property
    @abstractmethod
    def model(self):
        pass

    @property
    @abstractmethod
    def mainLabels(self):
        pass

    @property
    @abstractmethod
    def labels(self):
        pass
