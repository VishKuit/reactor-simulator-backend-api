from models.reactors.module import ReactorModule


class CSTR(ReactorModule):
    def __init__(self, reactor):
        self.__reactor = reactor

    # TODO: Implement method
    def inital_calculations(self):
        raise NotImplementedError("Method not implemented yet")

    # TODO: Implement method
    def temp_press_equations(self):
        raise NotImplementedError("Method not implemented yet")

    # TODO: Implement method
    @property
    def model(self):
        raise NotImplementedError("Method not implemented yet")

    # TODO: Implement method
    @property
    def mainLabels(self):
        raise NotImplementedError("Method not implemented yet")

    # TODO: Implement method
    @property
    def labels(self):
        raise NotImplementedError("Method not implemented yet")
