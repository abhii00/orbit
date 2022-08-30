from utils import dotdict

'''
M: 1/100 M_S = 1.9889e+28 kg
L: 1/10 AU = 1.496e+10 m
T: 1 Days = 86400 s
'''

consts = {
    'G': 6.674e-11
}
consts = dotdict(consts)

units = {
    'M': 1.989e+28,
    'L': 1.496e+10,
    'T': 86400
}
units = dotdict(units)

disp = {
    'R': 1000
}
disp = dotdict(disp)