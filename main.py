import pygame as pyg
from universe import Universe
from data import microSolarSystem

#TODO Add collisions
#TODO Add solar system dataset
#TODO Add unit converter
#TODO Add controllable spacecraft
#TODO Add orbit prediction

if __name__ == '__main__':
    pyg.init()
    x = Universe(800, 800, microSolarSystem)
    x.simulate(0.5, 2000)