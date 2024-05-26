import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)



def get_data():

    data = request.get_json()

     # obtener los datos enviados desde Vue.js

    # asignar los valores recibidos a las variables correspondientes
    RT = data.get('RT', 0)
    p0 = data.get('p0', 0)
    t0 = data.get('t0', 0)
    yA0 = data.get('yA0', 0)
    yB0 = data.get('yB0', 0)
    yC0 = data.get('yC0', 0)
    yD0 = data.get('yD0', 0)
    a = data.get('a', 0)
    b = data.get('b', 0)
    c = data.get('c', 0)
    d = data.get('d', 0)
    Ea = data.get('Ea', 0)
    A = data.get('A', 0)
    caidaPresion = data.get('caidaPresion', False)
    caidaTemperatura = data.get('caidaTemperatura', False)
    FT0 = data.get('FT0', 0)
    NT0 = data.get('NT0', 0)
    V = data.get('V', 0)
    CA = data.get('CA', "")
    CB = data.get('CB', "")
    CC = data.get('CC', "")
    CD = data.get('CD', "")
    ra = data.get('ra', "")
    Ratm = 0.08205746

    Rjmol = 8.314472

    return [p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V]

def model_PFR_flux(F, V):

    p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V = get_data()

    FA, FB, FC, FD, P, T = F

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

    dPdV = 0

    dTdV = 0

    if(caidaPresion == True):
        dPdV = 'Placeholder' # -> input
    else:
        dPdV = 0 # No Input
        P = p0

    if(caidaTemperatura == True):
        dTdV = 'Placeholder' # -> input
    else:
        dTdV = 0 # No Input
        T = t0

    FT = FA + FB + FC + FD

    yA = FA / FT
    yB = FB / FT
    yC = FC / FT
    yD = FD / FT

    formulas_c = c_formulas()

    CA = eval(formulas_c[0])
    CB = eval(formulas_c[1])
    CC = eval(formulas_c[2])
    CD = eval(formulas_c[3])

    ra_formula = formula_ra()

    dFAdV = rA = eval(ra_formula)
    dFBdV = rB = rA * (b/a)
    dFCdV = rC = rA * (c/a)
    dFDdV = rD = rA * (d/a)

    return [dFAdV, dFBdV, dFCdV, dFDdV, dPdV, dTdV]

def model_PFR_Conversion(F, V):

    p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V = get_data()

    X, P, T = F

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

    dPdV = 0

    dTdV = 0

    if(caidaPresion == True):
        dPdV = 'Placeholder' # -> input
    else:
        dPdV = 0 # No Input
        P = p0

    if(caidaTemperatura == True):
        dTdV = 'Placeholder' # -> input
    else:
        dTdV = 0 # No Input
        T = t0

    formulas_c = c_formulas()

    CA = eval(formulas_c[0])
    CB = eval(formulas_c[1])
    CC = eval(formulas_c[2])
    CD = eval(formulas_c[3])

    ra_formula = formula_ra()

    rA = eval(ra_formula)
    rB = rA * (b/a)
    rC = rA * (c/a)
    rD = rA * (d/a)

    dXdV = -rA/FA0

    return [dXdV, dPdV, dTdV]

def model_PBR_flux(F, W):

    p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V = get_data()

    FA, FB, FC, FD, P, T = W

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

    dPdW = 0

    dTdW = 0

    if(caidaPresion == True):
        dPdW = 'Placeholder' # -> input
    else:
        dPdW = 0 # No Input
        P = p0

    if(caidaTemperatura == True):
        dTdW = 'Placeholder' # -> input
    else:
        dTdW = 0 # No Input
        T = t0

    FT = FA + FB + FC + FD

    yA = FA / FT
    yB = FB / FT
    yC = FC / FT
    yD = FD / FT

    formulas_c = c_formulas()

    CA = eval(formulas_c[0])
    CB = eval(formulas_c[1])
    CC = eval(formulas_c[2])
    CD = eval(formulas_c[3])

    ra_formula = formula_ra()

    dFAdW = rA = eval(ra_formula)
    dFBdW = rB = rA * (b/a)
    dFCdW = rC = rA * (c/a)
    dFDdW = rD = rA * (d/a)

    return [dFAdW, dFBdW, dFCdW, dFDdW, dPdW, dTdW]

def model_PBR_Conversion(F, W):

    p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V = get_data()

    X, P, T = W

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

    dPdW = 0

    dTdW = 0

    if(caidaPresion == True):
        dPdW = 'Placeholder' # -> input
    else:
        dPdW = 0 # No Input
        P = p0

    if(caidaTemperatura == True):
        dTdW = 'Placeholder' # -> input
    else:
        dTdW = 0 # No Input
        T = t0

    formulas_c = c_formulas()

    CA = eval(formulas_c[0])
    CB = eval(formulas_c[1])
    CC = eval(formulas_c[2])
    CD = eval(formulas_c[3])

    ra_formula = formula_ra()

    rA = eval(ra_formula)
    rB = rA * (b/a)
    rC = rA * (c/a)
    rD = rA * (d/a)

    dXdW = -rA/FA0

    return [dXdW, dPdW, dTdW]

def model_Batch_flux(F, time):

    p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V = get_data()

    NA, NB, NC, ND, P, T = time

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

    NA0 = NT0 * yA0
    NB0 = NT0 * yB0
    NC0 = NT0 * yC0
    ND0 = NT0 * yD0

    K = A * np.exp(-Ea / (t0 * Rjmol))

    dPdtime = 0

    dTdtime = 0

    if(caidaPresion == True):
        dPdtime = 'Placeholder' # -> input
    else:
        dPdtime = 0 # No Input
        P = p0

    if(caidaTemperatura == True):
        dTdtime = 'Placeholder' # -> input
    else:
        dTdtime = 0 # No Input
        T = t0

    NT = NA + NB + NC + ND

    yA = NA / NT
    yB = NB / NT
    yC = NC / NT
    yD = ND / NT

    formulas_c = c_formulas()

    CA = eval(formulas_c[0])
    CB = eval(formulas_c[1])
    CC = eval(formulas_c[2])
    CD = eval(formulas_c[3])

    ra_formula = formula_ra()

    rA = eval(ra_formula)
    rB = rA * (b/a)
    rC = rA * (c/a)
    rD = rA * (d/a)

    dNAdt = -rA * V
    dNBdt = -rB * V
    dNCdt = -rC * V
    dNDdt = -rD * V

    return [dNAdt, dNBdt, dNCdt, dNDdt, dPdtime, dTdtime]

def model_Batch_Conversion(F, time):

    p0, t0, yA0, yB0, yC0, yD0, a, b, c, d, Ea, A, Ratm, Rjmol, caidaPresion, caidaTemperatura, FT0, NT0, V = get_data()

    X, P, T = time

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

    NA0 = NT0 * yA0
    NB0 = NT0 * yB0
    NC0 = NT0 * yC0
    ND0 = NT0 * yD0

    K = A * np.exp(-Ea / (t0 * Rjmol))

    dPdtime = 0

    dTdtime = 0

    if(caidaPresion == True):
        dPdtime = 'Placeholder' # -> input
    else:
        dPdtime = 0 # No Input
        P = p0

    if(caidaTemperatura == True):
        dTdtime = 'Placeholder' # -> input
    else:
        dPdtime = 0 # No Input
        T = t0

    formulas_c = c_formulas()

    CA = eval(formulas_c[0])
    CB = eval(formulas_c[1])
    CC = eval(formulas_c[2])
    CD = eval(formulas_c[3])

    ra_formula = formula_ra()

    rA = eval(ra_formula)
    rB = rA * (b/a)
    rC = rA * (c/a)
    rD = rA * (d/a)

    dXdtime = (-rA * V) / NA0 

    return [dXdtime, dPdtime, dTdtime]