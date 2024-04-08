import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# inputs "Datos de entrada"


# Calculo ecuacion diferencial
# Ecuacion: dFA/dV=rA

# Define the function for the differential equation
def model(F,V):

    P0          = 10
    T0          = 533.15
    FT0         = 1200
    yA0         = 0.67
    yB0         = 0.33
    yC0         = 0
    yD0         = 0
    yI0         = 1 - ( yA0 + yB0 + yC0 + yD0 )

    # Coeficientes estequiometricos
    a           = -1
    b           = -0.5
    c           = 1
    d           = 0

    # Constantes de velocidad
    k1          = 6.40

    # Caida de presion
    alfa        = 0

    # Calculo de datos Ratm=0.08205746 delta=(a/a+b/a+c/a) ε (epsilon)=delta*yA0 ΘA (thetaA)=yA0/yA0 ΘB (thetaB)=yB0/yA0 ΘC (thetaC)=yC0/yA0 ΘD (thetaD)=yD0/yA0 CT0=P0/(Ratm*T0) CA0=(P0*yA0)/(Ratm*T0) FT=FA+FB+FC+FD (Reactor SIN caida de presion ni temperatura) P=P0 T=T0

    # Constante de los gases ideales
    Ratm        = 0.08205746

    # Cambio de densidad
    delta       = (a/a) + (b/a) + (c/a) + (d/a)

    epsilon     = delta*yA0

    # Relación de la fracción y fracción del reactivo limitante
    thetaA      = yA0/yA0
    thetaB      = yB0/yA0
    thetaC      = yC0/yA0
    thetaD      = yD0/yA0

    CT0         = P0/(Ratm*T0)
    CA0         = (P0*yA0)/(Ratm*T0)

    FA0         = FT0 * yA0
    FB0         = FT0 * yB0
    FC0         = FT0 * yC0
    FD0         = FT0 * yD0

    # Assign each element of F to an individual variable
    FA, FB, FC, FD = F

    FT = FA + FB + FC + FD

    # Fraction
    yA = FA/FT
    yB = FB/FT
    yC = FC/FT
    yD = 0 # !only for this case

    # Concentracion en funcion del tiempo
    CA = (FA/FT) * CT0
    CB = (FB/FT) * CT0
    CC = (FC/FT) * CT0
    CD = (FD/FT) * CT0

    # Velocidad de reaccion
    rA = (-k1) * ((yA * P0) ** (1 / 3)) * ((yB * P0) ** (2 / 3))
    rB = rA * (b/a)
    rC = rA * (c/a)
    rD = rA * (d/a)

    # Ecuaciones diferenciales en base al tipo de reactor
    dFAdV = rA
    dFBdV = rB
    dFCdV = rC
    dFDdV = rD

    return [dFAdV, dFBdV, dFCdV, dFDdV]


# Time points
V = np.linspace(0, 140)  # adjust as needed


P0          = 10
T0          = 533.15
FT0         = 1200
yA0         = 0.67
yB0         = 0.33
yC0         = 0
yD0         = 0
yI0         = 1 - ( yA0 + yB0 + yC0 + yD0 )

FA0         = FT0 * yA0
FB0         = FT0 * yB0
FC0         = FT0 * yC0
FD0         = FT0 * yD0

F0 = [FA0, FB0, FC0, FD0]

# Solve ODE
F = odeint(model, F0, V, rtol=1e-6, atol=1e-6)

# Plot results
plt.plot(V, F[:, 0], label="FA")
plt.plot(V, F[:, 1], label="FB")
plt.plot(V, F[:, 2], label="FC")
plt.plot(V, F[:, 3], label="FD")
plt.xlabel("Volume (V)")
plt.ylabel("Concentration (F)")
plt.legend()


# Show the plot
plt.savefig("plot.png")
