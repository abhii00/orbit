import numpy as np
import pygame as pyg
import constants

class Universe:
    '''Class to hold the plottable universe.
    
    Parameters:
        windowHeight (int): the pixel height of the window
        windowWidth (int): the pixel width of the window
        celestialObjects (list): a list of the bodies in the universe
        explorer (Explorer): an explorer
        starrySky_number (int): number of stars in background
        starrySky_twinkleStep (int): period of star twinkle

    Returns:
        None
    '''

    def __init__(self, windowHeight = 800, windowWidth = 800, **kwargs):
        '''Initialisation.'''

        #init
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.celestialObjects = kwargs.get('celestialObjects', [])
        self.explorer = kwargs.get('explorer', None)
        self.explorerExists = True if self.explorer != None else False
        self.starrySky_number = kwargs.get("starrySky_number", 80)
        self.starrySky_twinkleStep = kwargs.get("starrySky_twinkleStep", 100)
        self.window = pyg.display.set_mode([self.windowHeight, self.windowWidth], pyg.DOUBLEBUF, 32)
        self.starrySky_positions = np.random.uniform(low=0,high=[self.windowWidth,self.windowHeight],size=(self.starrySky_number,2))
        self.starrySky_colors = [np.random.uniform(low=200, high=255) for star in self.starrySky_positions]
        self.starrySky_radii = np.random.randint(low=1,high=3,size=self.starrySky_number)
        self.starrySky_modifiers = np.random.rand(len(self.starrySky_colors))

        #simulate
        self.timeStep = 0
        self.timeTotal = 0
        self.timeEnd = 0
        self.timeStepTotal = 0
        self.simRunning = False

    def simulate(self, timeStep, timeEnd):
        '''Simulates the motion.
        
        Parameters:
            timeStep (float): the simulation time step (in true units)
            timeEnd (float): the simulation time end (in true units)
        Returns:
            None
        '''

        self.timeStep = timeStep
        self.timeTotal = 0
        self.timeEnd = timeEnd
        self.simRunning = True

        while self.simRunning:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.simRunning = False

            self._draw()
            self._move()

            self.timeTotal += self.timeStep
            self.timeStepTotal += 1

            if self.timeTotal >= self.timeEnd: self.simRunning = False

    def forces(self, mainObject):
        '''Calculates the forces on the body.
        
        Parameters:
            mainObject (celestialObject): the body for which to calculate forces
        Returns:
            F (np array): 2d vector of the forces (in true units)
        '''

        F = np.array([0, 0, 0], dtype='float64')

        for celestialObject in self.celestialObjects:
            if np.linalg.norm(celestialObject.position - mainObject.position) > 0.00000001:
                r = (celestialObject.position - mainObject.position)
                
                F += (constants.consts.G * celestialObject.mass * mainObject.mass / np.linalg.norm(r)**2) * (r / np.linalg.norm(r))
        
        return F

    def _move(self):
        '''Updates the position and motion of the bodies.'''

        for celestialObject in self.celestialObjects:
            celestialObject.move(self.forces, self.timeStep)

        if self.explorerExists: self.explorer.move(self.forces, self.timeStep)
    
    def _draw(self):
        '''Updates the window.'''
        self.window.lock()
        self.window.fill((0,0,0))

        if self.timeStepTotal % self.starrySky_twinkleStep == 0:
           self.starrySky_modifiers = np.random.rand(len(self.starrySky_colors)) 

        for i, star_position in enumerate(self.starrySky_positions):
            star_color = self.starrySky_colors[i] * self.starrySky_modifiers[i]
            star_radius = self.starrySky_radii[i]
            pyg.draw.circle(self.window, (star_color, star_color, star_color), star_position, star_radius)

        for celestialObject in self.celestialObjects:
            celestialObject.draw(self.window)

        if self.explorerExists: self.explorer.draw(self.window)
        
        self.window.unlock()
        pyg.display.update()