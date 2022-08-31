import numpy as np
from utils import dotdict

consts = {
    'G': 6.674e-11,
    'M_s': 1.989e+30,
    'M_e': 5.972e+24,
    'AU': 1.496e+11,
    'R_s': 6.957e+8,
    'R_e': 6.371e+6,
    'T_e': 86400 
}
consts = dotdict(consts)

units = {
    'M': consts.M_s/100,
    'L': consts.AU/50,
    'T': consts.T_e/2
}
units = dotdict(units)

def Rscale(val):
    return 2*np.abs(np.arctan(10000*val))

disp = {
    'R': Rscale
}
disp = dotdict(disp)