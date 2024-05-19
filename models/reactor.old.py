import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class Reactor:

    #
    def __init__(self):
        self.__seted_up = False
        self.__model = None
        self.rAtm = 0.08206
        self.rJmol = 8.314

    # Define the initial conditions
    def setup_reactor(
        self,
        RT,
        FNV,
        VT,
        P0,
        T0,
        yA0,
        yB0,
        yC0,
        yD0,
        a,
        b,
        c,
        d,
        EA,
        A,
        rA,
        CEq=None,
        pd=False,
        td=False,
        pd_eq=None,
        td_eq=None,
    ):
        self.__ReactorType = RT
        self.__FNV = FNV
        self.__VariableType = VT
        self.__P0 = P0
        self.__T0 = T0
        self.__yA0 = yA0
        self.__yB0 = yB0
        self.__yC0 = yC0
        self.__yD0 = yD0
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d
        self.__EA = EA
        self.__ArrConst = A
        self.__rA = rA
        self.__CEq = CEq
        self.__pd = pd
        self.__td = td
        self.__pd_eq = pd_eq
        self.__td_eq = td_eq
        self.__run_initial_calculations()
        self.__temperature_pressure_equations()
        self.__asign_model()

        self.__seted_up = True

    def __temperature_pressure_equations(self):
        # If RT is PFR, and there is pressure drop
        # then define dPdV from pd_eq
        if self.__ReactorType == 2:
            if self.__pd:
                self.__dPdV = self.__pd_eq
            else:
                self.__dPdV = 0

            if self.__td:
                self.__dTdV = self.__td_eq
            else:
                self.__dTdV = 0

        #

    def __run_initial_calculations(self):
        # If reactor type is PFR, PBR, CSTR
        # then FT0 is equal to FNV
        # if not, NT0 and V are equal to FNV[0] and FNV[1] respectively
        if (
            self.__ReactorType == 2
            or self.__ReactorType == 3
            or self.__ReactorType == 1
        ):
            self.__FT0 = self.__FNV
        else:
            self.__NT0, self.__V = self.__FNV

        # If PFR and variable type is conversion
        # then F0 is equal to [X0, P0, T0]
        if self.__ReactorType == 2 and self.__VariableType == 1:
            self.__F0 = [0, self.__P0, self.__T0]

        # # If reactor type is not CSTR
        # # then define CA, CB, CC, CD from CEq
        # if self.__ReactorType != 1:
        #     self.__CA, self.__CB, self.__CC, self.__CD = self.__CEq

        # #
        # self.__yI0 = 1 - (self.__yA0 + self.__yB0 + self.__yC0 + self.__yD0)

        # # Ratio of the fraction and fraction of the limiting reactant
        # self.__thetaA      = self.__yA0/self.__yA0
        # self.__thetaB      = self.__yB0/self.__yA0
        # self.__thetaC      = self.__yC0/self.__yA0
        # self.__thetaD      = self.__yD0/self.__yA0

        # # Initial concentrations
        # self.__CT0         = self.__P0/(self.rAtm*self.__T0)
        # self.__CA0         = (self.__P0*self.__yA0)/(self.rAtm*self.__T0)

        # Initial molar flow rates
        self.__FA0 = self.__FT0 * self.__yA0
        # self.__FB0         = self.__FT0 * self.__yB0
        # self.__FC0         = self.__FT0 * self.__yC0
        # self.__FD0         = self.__FT0 * self.__yD0
        # self.__F0 = [self.__FA0, self.__FB0, self.__FC0, self.__FD0, self.__P0]

    # Private models
    def __model_convertion_pfr(self, F, V):
        # Assign each element of F to an individual variable
        X, P, T = F

        #
        self.__rB = self.__rA * (self.__b / self.__a)
        self.__rC = self.__rA * (self.__c / self.__a)
        self.__rD = self.__rA * (self.__d / self.__a)

        dXdV = -self.__rA / self.__FA0

        return [dXdV, self.__dPdV, self.__dTdV]

    # def __model(self, F, V):
    #     reactor_model = None

    #     # TODO: si es variable de conversión
    #     if True:

    #     # TODO: si es variable de flujo
    #     if True:
    #         # Assign each element of F to an individual variable
    #         FA, FB, FC, FD, P = F

    #         # Total molar flow rate
    #         FT = FA + FB + FC + FD

    #         # Mole fractions
    #         yA = FA/FT
    #         yB = FB/FT
    #         yC = FC/FT
    #         yD = 0 # !only for this case

    #         # Concentration as a function of time
    #         CA = (FA/FT) * self.__CT0
    #         CB = (FB/FT) * self.__CT0
    #         CC = (FC/FT) * self.__CT0
    #         CD = (FD/FT) * self.__CT0

    #         # Reaction rates
    #         rA = (-self.__k1) * ((yA * self.__P0) ** (1 / 3)) * ((yB * self.__P0) ** (2 / 3))
    #         rB = rA * (self.__b/self.__a)
    #         rC = rA * (self.__c/self.__a)
    #         rD = rA * (self.__d/self.__a)

    #         # Differential equations based on the type of reactor
    #         dFAdV = rA
    #         dFBdV = rB
    #         dFCdV = rC
    #         dFDdV = rD

    #         dPdV = 0
    #         # Pressure drop
    #         if self.__pd == 1:
    #             dPdV = FA

    #         reactor_model = [dFAdV, dFBdV, dFCdV, dFDdV, dPdV]

    #     # Return the differentials
    #     return reactor_model

    def __asign_model(self):
        # If reactor type is PFR and variable type is conversion
        # then assign the model to __model_convertion_pfr
        if self.__ReactorType == 2 and self.__VariableType == 1:
            self.__model = self.__model_convertion_pfr

    def __plot_results(self, V, F):
        # Plot the results
        plt.plot(V, F[:, 0], label="X")
        plt.plot(V, F[:, 1], label="P")
        plt.plot(V, F[:, 2], label="T")
        # plt.plot(V, F[:, 0], label="FA")
        # plt.plot(V, F[:, 1], label="FB")
        # plt.plot(V, F[:, 2], label="FC")
        # plt.plot(V, F[:, 3], label="FD")
        # plt.plot(V, F[:, 4], label="P")
        plt.xlabel("Volume (V)")
        plt.ylabel("Concentration (F)")
        plt.legend()

        # Save the plot
        plt.savefig("plot.png")

    def run(self):
        # If the reactor is not set up, raise an error
        if not self.__seted_up:
            raise Exception(
                "The reactor is not set up. Please run setup_reactor() first."
            )

        V = np.linspace(0, 140)  # adjust as needed
        F = odeint(self.__model, self.__F0, V, rtol=1e-6, atol=1e-6)
        self.__plot_results(V, F)


# Test the reactor
reactor = Reactor()
# reactor.setup_reactor(RT=2, VT=1, P0=10, T0=533.15, FT0=1200, yA0=0.67, yB0=0.33, yC0=0, yD0=0, a=-1, b=-0.5, c=1, d=0, k1=6.40, pd=0, td=0)
reactor.setup_reactor(
    RT=2,
    FNV=1200,
    VT=1,
    P0=10,
    T0=533.15,
    yA0=0.67,
    yB0=0.33,
    yC0=0,
    yD0=0,
    a=-1,
    b=-0.5,
    c=1,
    d=0,
    EA=6.40,
    A=1,
    rA=1,
    CEq=[0, 0, 0, 0],
    pd=False,
    td=False,
    pd_eq=None,
    td_eq=None,
)
reactor.run()
