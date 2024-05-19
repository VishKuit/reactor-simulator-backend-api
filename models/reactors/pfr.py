from models.reactors.module import ReactorModule


class PFR(ReactorModule):
    def __init__(self, reactor):
        self.__reactor = reactor

    def inital_calculations(self):
        self.__reactor.FT0 = self.__reactor.FNV
        self.__reactor.FA0 = self.__reactor.FT0 * self.__reactor.yA0

        # TODO: currently CA is not being used
        # self.__reactor.CA, self.__reactor.CB, self.__reactor.CC, self.__reactor.CD = self.__reactor.CEq

        # if variable is convertion
        if self.__reactor.VariableType == 1:
            self.__reactor.F0 = [0, self.__reactor.P0, self.__reactor.T0]
            self.__model = self.convertion_model

            self.__mainLabels = ['Volume (V)', 'Concentration (F)']
            self.__labels = ['X', 'P', 'T']
        else: # Flow
            self.__model = self.flow_model

            self.__mainLabels = ['Unknown', 'Unknown']
            self.__labels = ['FA', 'FB', 'FC', 'FD', 'P', 'T']

        # Initial molar flow rates
        self.__reactor.FA0 = self.__reactor.FT0 * self.__reactor.yA0

    def temp_press_equations(self):
        self.__reactor.dPdV = self.__reactor.pd_eq if self.__reactor.pd_eq is not None else 0
        self.__reactor.dTdV = self.__reactor.td_eq if self.__reactor.td_eq is not None else 0

    @property
    def model(self):
        return self.__model

    @property
    def mainLabels(self):
        return self.__mainLabels

    @property
    def labels(self):
        return self.__labels

    def convertion_model(self, F, V):
        X, P, T = F

        #
        self.__reactor.rB = self.__reactor.rA * (self.__reactor.b / self.__reactor.a)
        self.__reactor.rC = self.__reactor.rA * (self.__reactor.c / self.__reactor.a)
        self.__reactor.rD = self.__reactor.rA * (self.__reactor.d / self.__reactor.a)

        self.__reactor.dXdV = self.__reactor.rA / self.__reactor.FA0
        return [self.__reactor.dXdV, self.__reactor.dPdV, self.__reactor.dTdV]

    # TODO: Implement method
    def flow_model(self):
        raise NotImplementedError("Method not implemented yet")
