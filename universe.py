import numpy as np
import pygame as pyg
import constants

class Universe:
    '''Class to hold the plottable universe.
    
    Parameters:
        windowHeight (int): the pixel height of the window
        windowWidth (int): the pixel width of the window
        celestialObjects (list): a list of the bodies in the universe

    Returns:
        None
    '''

    def __init__(self, windowHeight = 800, windowWidth = 800, celestialObjects = []):
        '''Initialisation.'''

        #init
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.celestialObjects = celestialObjects
        self.window = pyg.display.set_mode([self.windowHeight, self.windowWidth], pyg.DOUBLEBUF, 32)

        #simulate
        self.timeStep = 0
        self.timeTotal = 0
        self.timeEnd = 0
        self.simRunning = False

    def simulate(self, timeStep, timeEnd):
        '''Simulates the motion.
        
        Parameters:
            timeStep (float): the simulation time step
            timeEnd (float): the simulation time end
        Returns:
            None
        '''

        self.timeStep = timeStep
        self.timeTotal = 0
        self.timeEnd = timeEnd
        self.simRunning = True

        while self.simRunning:
            self._draw()
            self._move()
            self.timeTotal += self.timeStep

            if self.timeTotal >= self.timeEnd: self.simRunning = False

    def forces(self, mainObject):
        '''Calculates the forces on the body.
        
        Parameters:
            mainObject (celestialObject): the body for which to calculate forces
        Returns:
            F (np array): 2d vector of the forces (in true units)
        '''

        F = np.array([0, 0], dtype='float64')

        for celestialObject in self.celestialObjects:
            if np.linalg.norm(celestialObject.position - mainObject.position) > 0.00000001:
                M = celestialObject.mass * constants.units.M
                m = mainObject.mass * constants.units.M
                r = (celestialObject.position - mainObject.position) * constants.units.L
                
                F += (constants.consts.G * M * m / np.linalg.norm(r)**2) * (r / np.linalg.norm(r))
        
        return F

    def _move(self):
        '''Updates the position and motion of the bodies.'''

        for celestialObject in self.celestialObjects:
            celestialObject.move(self.forces, self.timeStep)

    def _draw(self):
        '''Updates the window.'''

        self.window.fill((0,0,0))

        for celestialObject in self.celestialObjects:
            celestialObject.draw(self.window)
            pyg.display.update()