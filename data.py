import numpy as np
import constants
from celestialobject import CelestialObject
from explorer import Explorer

microSolarSystem = [
    CelestialObject(constants.consts.M_s, constants.consts.R_s, (255, 255, 255), 
                    np.array([400, 400, 0]) * constants.units.L, [0, 0, 0]), #sun
    CelestialObject(0.330e24, 2438e3, (231, 232, 236),
                    np.array([400, 400, 0]) * constants.units.L + np.array([49.0e9, 0, 0]), np.array([0, 47.4e3, 0])), #mercury
    CelestialObject(constants.consts.M_e, constants.consts.R_e, (107, 147, 214), 
                    np.array([400, 400, 0])  * constants.units.L + np.array([constants.consts.AU, 0, 0]), np.array([0, 30e3, 0])), #earth
    CelestialObject(1898e24, 71492e3, (201, 144, 57),
                    np.array([400, 400, 0])  * constants.units.L + np.array([778.5e9, 0, 0]), np.array([0, 13.1e3, 0])), #jupiter
    CelestialObject(1898e24, 71492e3, (201, 144, 57),
                    np.array([400, 400, 0])  * constants.units.L + np.array([-778.5e9, 0, 0]), np.array([0, 0, 13.1e3])) #fakiter
]

microExplorer = Explorer(10000, constants.consts.R_s*100, (255, 0, 0), 
                        np.array([400, 400, 0])  * constants.units.L - np.array([-46.0e9, 0, 0]), np.array([0, 47.4e3, 0]), np.array([0, 0, 0]))