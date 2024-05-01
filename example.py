import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# User inputs

# RT: Reactor type
try:
    RT = int(input("Enter the reactor type (1 for CSTR, 2 for PFR, 3 for PBR and 4 for Batch): "))
except ValueError:
    print("Invalid input. Leaving the default value: 2.")
    RT = 2

# Only RT = 2 is currently supported
if RT != 2:
    print("Only RT = 2 is currently supported. Exiting the program.")
    exit()

# P0
try:
    P0 = int(input("Enter a value for P0: "))
except ValueError:
    print("Invalid input. Leaving the default value: 10.")
    P0 = 10

# T0
try:
    T0 = float(input("Enter a value for T0: "))
except ValueError:
    print("Invalid input. Leaving the default value: 533.15.")
    T0 = 533.15

# FT0
try:
    FT0 = int(input("Enter a value for FT0: "))
except ValueError:
    print("Invalid input. Leaving the default value: 1200.")
    FT0 = 1200

# yA0
try:
    yA0 = float(input("Enter a value for yA0: "))
except ValueError:
    print("Invalid input. Leaving the default value: 0.67.")
    yA0 = 0.67

# yB0
try:
    yB0 = float(input("Enter a value for yB0: "))
except ValueError:
    print("Invalid input. Leaving the default value: 0.33.")
    yB0 = 0.33

# yC0
try:
    yC0 = float(input("Enter a value for yC0: "))
except ValueError:
    print("Invalid input. Leaving the default value: 0.")
    yC0 = 0

# yD0
try:
    yD0 = float(input("Enter a value for yD0: "))
except ValueError:
    print("Invalid input. Leaving the default value: 0.")
    yD0 = 0


# Coeficientes estequiometricos

# a
try:
    a = float(input("Enter a value for a: "))
except ValueError:
    print("Invalid input. Leaving the default value: -1.")
    a = -1

# b
try:
    b = float(input("Enter a value for b: "))
except ValueError:
    print("Invalid input. Leaving the default value: -0.5.")
    b = -0.5

# c
try:
    c = float(input("Enter a value for c: "))
except ValueError:
    print("Invalid input. Leaving the default value: 1.")
    c = 1

# d
try:
    d = float(input("Enter a value for d: "))
except ValueError:
    print("Invalid input. Leaving the default value: 0.")
    d = 0



# Constantes de velocidad
# k1
try:
    k1 = float(input("Enter a value for k1 (constante de velocidad): "))
except ValueError:
    print("Invalid input. Leaving the default value: 6.40.")
    k1 = 6.40


# pd: Presure drop (1 si, 0 no)
# pd
try:
    pd = int(input("Enter a value for pd (pressure drop): 1 for yes, 0 for no: "))
except ValueError:
    print("Invalid input. Leaving the default value: 0.")
    pd = 0


# Define eqdrop dinamically depending on the value of pd and the reactor type (RT)
# Match case
if pd == 1:
    match RT:
        case 1:
            eqdrop = ""
        case 2:
            eqdrop = ""
        case 3:
            eqdrop = ""
        case 4:
            eqdrop = ""



# Calculations:
# Constante de los gases ideales
Ratm = 0.08205746
#
yI0 = 1 - (yA0 + yB0 + yC0 + yD0)
# Ratio of the fraction and fraction of the limiting reactant
thetaA      = yA0/yA0
thetaB      = yB0/yA0
thetaC      = yC0/yA0
thetaD      = yD0/yA0

# Initial concentrations
CT0         = P0/(Ratm*T0)
CA0         = (P0*yA0)/(Ratm*T0)


# Initial molar flow rates
FA0         = FT0 * yA0
FB0         = FT0 * yB0
FC0         = FT0 * yC0
FD0         = FT0 * yD0


# Define the function for the differential equation
def model(F,V):
    # Assign each element of F to an individual variable
    FA, FB, FC, FD, P = F

    # Total molar flow rate
    FT = FA + FB + FC + FD

    # Mole fractions
    yA = FA/FT
    yB = FB/FT
    yC = FC/FT
    yD = 0 # !only for this case

    # Concentration as a function of time
    CA = (FA/FT) * CT0
    CB = (FB/FT) * CT0
    CC = (FC/FT) * CT0
    CD = (FD/FT) * CT0

    # Reaction rates
    rA = (-k1) * ((yA * P0) ** (1 / 3)) * ((yB * P0) ** (2 / 3))
    rB = rA * (b/a)
    rC = rA * (c/a)
    rD = rA * (d/a)

    # Differential equations based on the type of reactor
    dFAdV = rA
    dFBdV = rB
    dFCdV = rC
    dFDdV = rD

    dPdV = 0
    # Pressure drop
    if pd == 1:
        dPdV = FA


    return [dFAdV, dFBdV, dFCdV, dFDdV, dPdV]

# Time points
V = np.linspace(0, 140)  # adjust as needed

# Initial conditions
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

F0 = [FA0, FB0, FC0, FD0, P0]

# Solve ODE
F = odeint(model, F0, V, rtol=1e-6, atol=1e-6)

# Plot results
plt.plot(V, F[:, 0], label="FA")
plt.plot(V, F[:, 1], label="FB")
plt.plot(V, F[:, 2], label="FC")
plt.plot(V, F[:, 3], label="FD")
plt.plot(V, F[:, 4], label="P")
plt.xlabel("Volume (V)")
plt.ylabel("Concentration (F)")
plt.legend()

# Save the plot
plt.savefig("plot.png")
