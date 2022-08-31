import pygame as pyg
from universe import Universe
from data import microSolarSystem

if __name__ == '__main__':
    pyg.init()
    x = Universe(800, 800, microSolarSystem)
    x.simulate(0.5, 2000)