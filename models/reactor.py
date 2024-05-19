import numpy as np
from scipy.integrate import odeint
from models.reactors.pfr import PFR
from models.reactors.pbr import PBR
from models.reactors.cstr import CSTR
from models.reactors.batch import Batch
import datetime
import matplotlib.pyplot as plt

class Reactor:

    #
    def __init__(self):
        pass

    def setup_reactor(
        self,
        RT: int,
        FNV: float,
        VT: int,
        P0: float,
        T0: float,
        yA0: float,
        yB0: float,
        yC0: float,
        yD0: float,
        a: float,
        b: float,
        c: float,
        d: float,
        EA: float,
        A: float,
        rA: float,
        ti: float = 0,
        tf: float = 500,
        CEq: str = None,
        pd_eq: str = None,
        td_eq: str = None,
    ):
        self.__set_initial_object_values(RT, FNV, VT, P0, T0, yA0, yB0, yC0, yD0, a, b, c, d, EA, A, rA, ti, tf, CEq, pd_eq, td_eq)
        self.__RTModule.inital_calculations()
        self.__RTModule.temp_press_equations()
        self.__seted_up = True

    def run(self):
        if not self.__seted_up:
            raise Exception("Reactor not set up yet")

        self.__xAxis = np.linspace(self.__ti, self.__tf)
        self.__allF = odeint(
            self.__RTModule.model, self.__F0, self.__xAxis, rtol=1e-7, atol=1e-7
        )

        self.__results = True

    def plot(self):
        if not self.__results:
            raise Exception("No results to plot")

        # For each label in self.__RTModule.labels
        # plot the corresponding data in allF
        for i in range(len(self.__RTModule.labels)):
            plt.plot(self.__xAxis, self.__allF[:, i], label=self.__RTModule.labels[i])

        plt.xlabel(self.__RTModule.mainLabels[0])
        plt.ylabel(self.__RTModule.mainLabels[1])
        plt.legend()

        # Create unique hash value for the file name
        hash_value = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        plt.savefig(f"static/{hash_value}.png")

    def __set_initial_object_values(self, RT, FNV, VT, P0, T0, yA0, yB0, yC0, yD0, a, b, c, d, EA, A, rA, ti, tf, CEq, pd_eq, td_eq):
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
        self.__ti = ti
        self.__tf = tf
        self.__CEq = CEq
        self.__pd_eq = pd_eq
        self.__td_eq = td_eq

        # Other initial values
        self.__FT0 = None
        self.__results = None

        # Assign RTModule to the corresponding reactor type
        # for example, if RT is 2 (PFR), then RTModule is an instance of PFR
        # (1 for CSTR, 2 for PFR, 3 for PBR and 4 for Batch)
        if self.__ReactorType == 1:
            self.__RTModule = CSTR(self)

        elif self.__ReactorType == 2:
            self.__RTModule = PFR(self)

        elif self.__ReactorType == 3:
            self.__RTModule = PBR(self)

        elif self.__ReactorType == 4:
            self.__RTModule = Batch(self)

    @property
    def ReactorType(self):
        return self.__ReactorType

    @ReactorType.setter
    def ReactorType(self, value):
        self.__ReactorType = value

    @property
    def FNV(self):
        return self.__FNV

    @FNV.setter
    def FNV(self, value):
        self.__FNV = value

    @property
    def F0(self):
        return self.__F0

    @F0.setter
    def F0(self, value):
        self.__F0 = value

    @property
    def FA0(self):
        return self.__FA0

    @FA0.setter
    def FA0(self, value):
        self.__FA0 = value

    @property
    def FT0(self):
        return self.__FT0

    @FT0.setter
    def FT0(self, value):
        self.__FT0 = value

    @property
    def VariableType(self):
        return self.__VariableType

    @VariableType.setter
    def VariableType(self, value):
        self.__VariableType = value

    @property
    def P0(self):
        return self.__P0

    @P0.setter
    def P0(self, value):
        self.__P0 = value

    @property
    def T0(self):
        return self.__T0

    @T0.setter
    def T0(self, value):
        self.__T0 = value

    @property
    def yA0(self):
        return self.__yA0

    @yA0.setter
    def yA0(self, value):
        self.__yA0 = value

    @property
    def yB0(self):
        return self.__yB0

    @yB0.setter
    def yB0(self, value):
        self.__yB0 = value

    @property
    def yC0(self):
        return self.__yC0

    @yC0.setter
    def yC0(self, value):
        self.__yC0 = value

    @property
    def yD0(self):
        return self.__yD0

    @yD0.setter
    def yD0(self, value):
        self.__yD0 = value

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = value

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = value

    @property
    def c(self):
        return self.__c

    @c.setter
    def c(self, value):
        self.__c = value

    @property
    def d(self):
        return self.__d

    @d.setter
    def d(self, value):
        self.__d = value

    @property
    def EA(self):
        return self.__EA

    @EA.setter
    def EA(self, value):
        self.__EA = value

    @property
    def ArrConst(self):
        return self.__ArrConst

    @ArrConst.setter
    def ArrConst(self, value):
        self.__ArrConst = value

    @property
    def rA(self):
        return self.__rA

    @rA.setter
    def rA(self, value):
        self.__rA = value

    @property
    def rB(self):
        return self.__rB

    @rB.setter
    def rB(self, value):
        self.__rB = value

    @property
    def rC(self):
        return self.__rC

    @rC.setter
    def rC(self, value):
        self.__rC = value

    @property
    def rD(self):
        return self.__rD

    @rD.setter
    def rD(self, value):
        self.__rD = value

    @property
    def CEq(self):
        return self.__CEq

    @CEq.setter
    def CEq(self, value):
        self.__CEq = value

    @property
    def pd_eq(self):
        return self.__pd_eq

    @pd_eq.setter
    def pd_eq(self, value):
        self.__pd_eq = value

    @property
    def td_eq(self):
        return self.__td_eq

    @td_eq.setter
    def td_eq(self, value):
        self.__td_eq = value

    @property
    def RTModule(self):
        return self.__RTModule

    @RTModule.setter
    def RTModule(self, value):
        self.__RTModule = value

    @property
    def CA(self):
        return self.__CA

    @CA.setter
    def CA(self, value):
        self.__CA = value

    @property
    def CB(self):
        return self.__CB

    @CB.setter
    def CB(self, value):
        self.__CB = value

    @property
    def CC(self):
        return self.__CC

    @CC.setter
    def CC(self, value):
        self.__CC = value

    @property
    def CD(self):
        return self.__CD

    @CD.setter
    def CD(self, value):
        self.__CD = value

    @property
    def dPdV(self):
        return self.__dPdV

    @dPdV.setter
    def dPdV(self, value):
        self.__dPdV = value

    @property
    def dTdV(self):
        return self.__dTdV

    @dTdV.setter
    def dTdV(self, value):
        self.__dTdV = value

    @property
    def dXdV(self):
        return self.__dXdV

    @dXdV.setter
    def dXdV(self, value):
        self.__dXdV = value

    @property
    def results(self):
        return self.__results

    # @results.setter
    # def results(self, value):
    #     self.__results = value


# OLD TESTING
# # Test the reactor
# reactor = Reactor()
# # reactor.setup_reactor(RT=2, VT=1, P0=10, T0=533.15, FT0=1200, yA0=0.67, yB0=0.33, yC0=0, yD0=0, a=-1, b=-0.5, c=1, d=0, k1=6.40, pd=0, td=0)
# reactor.setup_reactor(
#     RT=2,
#     FNV=1200,
#     VT=1,
#     P0=10,
#     T0=533.15,
#     yA0=0.67,
#     yB0=0.33,
#     yC0=0,
#     yD0=0,
#     a=-1,
#     b=-0.5,
#     c=1,
#     d=0,
#     EA=6.40,
#     A=1,
#     rA=1,
#     CEq=[0, 0, 0, 0],
#     pd=False,
#     td=False,
#     pd_eq=None,
#     td_eq=None,
# )
# reactor.run()

# NEW TESTING
reactor = Reactor()
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
    ti=0,
    tf=140,
    CEq=None,
    pd_eq=None,
    td_eq=None
)
reactor.run()
reactor.plot()
