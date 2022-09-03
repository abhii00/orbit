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
        self.center = np.zeros(3)
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
        self.timeStep_original = self.timeStep
        self.timeTotal = 0
        self.timeEnd = 0
        self.timeStepTotal = 0
        self.simRunning = False
        self.keysPressed = []
        self.displayMode = '2D'

    def simulate(self, timeStep, timeEnd):
        '''Simulates the motion.
        
        Parameters:
            timeStep (float): the simulation time step (in true units)
            timeEnd (float): the simulation time end (in true units)
        Returns:
            None
        '''

        self.timeStep = timeStep
        self.timeStep_original = self.timeStep
        self.timeTotal = 0
        self.timeEnd = timeEnd
        self.simRunning = True

        while self.simRunning:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.simRunning = False
            self.keysPressed = pyg.key.get_pressed()

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
            if np.linalg.norm(celestialObject.position - mainObject.position) > celestialObject.radius + mainObject.radius:
                r = (celestialObject.position - mainObject.position)
                F += (constants.consts.G * celestialObject.mass * mainObject.mass / np.linalg.norm(r)**2) * (r / np.linalg.norm(r))
        
        return F

    def _move(self):
        '''Updates the position and motion of the bodies.'''

        for celestialObject in self.celestialObjects: celestialObject.move(self.forces, self.timeStep)

        if self.explorerExists: self.explorer.move(self.forces, self.timeStep, self.keysPressed)
    
    def _draw(self):
        '''Updates the window.'''
        self.window.lock()
        self.window.fill((0,0,0))

        if self.displayMode == '2D':

            if self.timeStepTotal % self.starrySky_twinkleStep == 0:
                self.starrySky_modifiers = np.random.rand(len(self.starrySky_colors)) 

            for i, star_position in enumerate(self.starrySky_positions):
                star_color = self.starrySky_colors[i] * self.starrySky_modifiers[i]
                star_radius = self.starrySky_radii[i]
                pyg.draw.circle(self.window, (star_color, star_color, star_color), star_position, star_radius)

            for celestialObject in self.celestialObjects: 
                pyg.draw.circle(self.window, celestialObject.color, celestialObject.position[:2] / constants.units.L, 
                                constants.disp.R(celestialObject.radius / constants.units.L))
                pyg.draw.lines(self.window, celestialObject.trail_color, False, (celestialObject.trail[:,:2] / constants.units.L).tolist(), 
                                celestialObject.trail_thickness)

            if self.explorerExists: 
                pyg.draw.circle(self.window, self.explorer.color, self.explorer.position[:2] / constants.units.L, 
                                constants.disp.R(self.explorer.radius / constants.units.L))
                pyg.draw.lines(self.window, self.explorer.trail_color, False, (self.explorer.trail[:,:2] / constants.units.L).tolist(), 
                                self.explorer.trail_thickness)
        
        self.window.unlock()
        pyg.display.update()