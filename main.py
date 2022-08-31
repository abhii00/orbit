import pygame as pyg
import constants
from universe import Universe
from data import microSolarSystem, microExplorer

#TODO Add collisions
#TODO Add solar system dataset
#TODO Add controllable spacecraft
#TODO Add orbit prediction

if __name__ == '__main__':
    pyg.init()
    x = Universe(800, 800, microSolarSystem)
    x.addExplorer(microExplorer)
    x.simulate(0.5 * constants.units.T, 2000 * constants.units.T)