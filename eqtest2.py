import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def variableIngress():
    p0 = 0 # -> input Initial Pressure

    t0 = 0 # -> input Initial Temperature

    yA0 = 0 # -> input

    yB0 = 0 # -> input

    yC0 = 0 # -> input

    yD0 = 0 # -> input

    a = 0 # -> input

    b = 0 # -> input

    c = 0 # -> input

    d = 0 # -> input

    Ea = 0 # -> input

    A = 0 # -> input

    Ratm = 0.08205746

    Rjmol = 8.314472

    caidaPresion = True # -> input crear if para verificar si se ingresa o no

    caidaTemperatura = True # -> input crear if para verificar si se ingresa o no

    FT0 = 0 # -> input

    NT0 = 0 # -> input

    V = 0 # -> input

    return [p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V]

def c_formulas():

    CA, CB, CC, CD = ""

    # Inputs for all four of them

    return [CA, CB, CC, CD]

def formula_ra():

    ra = ""

    # Inputs for ra

    return ra

def model_PTR_flux(F, V):

    p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V = variableIngress()

    FA, FB, FC, FD, P = F

    yl0 = 1 - (yA0 + yB0 + yC0 + yD0)

    thetaA = yA0 / yA0
    thetaB = yB0 / yA0
    thetaC = yC0 / yA0
    thetaD = yD0 / yA0

    CT0 = p0 / (Ratm * t0)
    CA0 = (p0 * yA0) / (Ratm * t0)
    CB0 = CT0 * yB0
    CC0 = CT0 * yC0
    CD0 = CT0 * yD0

    FA0 = FT0 * yA0
    FB0 = FT0 * yB0
    FC0 = FT0 * yC0
    FD0 = FT0 * yD0

    K = A * np.exp(-Ea / (t0 * Rjmol))

    if(caidaPresion == True):
        P = p0
    else:
        P = 0 # -> input

    if(caidaTemperatura == True):
        T = t0
    else:
        T = 0 # -> input

    formulas_c = c_formulas()

    CA = eval(formulas_c[0])
    CB = eval(formulas_c[1])
    CC = eval(formulas_c[2])
    CD = eval(formulas_c[3])

    ra_formula = formula_ra()