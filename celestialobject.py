import numpy as np
import pygame as pyg
import constants

class CelestialObject:
    '''Class to hold a single star/planet/moon.
    
    Parameters:
        mass (float): the mass of the object (in scaled units)
        radius (float): the radius of the object (in scaled units)
        color (tuple): the color of the object
        position (np array): 2d vector of the position of the object (in scaled units)
        velocity (np array): 2d vector of the velocity of the object (in scaled units)
    Returns:
        None
    '''

    def __init__(self, mass, radius, color, position, velocity):
        #init
        self.mass = mass
        self.radius = radius
        self.color = color
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.acceleration = np.empty_like(position, dtype='float64')
    
    def draw(self, window):
        '''Draws the body onto a window.
        
        Parameters:
            window (pygame.display): the window onto which the body is drawn
        Returns:
            None
        '''

        pyg.draw.circle(window, self.color, self.position, self.radius*constants.disp.R)

    def move(self, F, timeStep):
        '''Updates the position and motion of the body.

        Parameters:
            F (np array): 2d vector of the forces on the body (in true units)
            timeStep (float): the time step size (in scaled units)
        '''
        m = self.mass * constants.units.M
        a = F(self)/m
        v = self.velocity * constants.units.L / constants.units.T
        r = self.position * constants.units.L
        dt = timeStep * constants.units.T

        r += v*dt + 0.5*a*dt**2
        a_new = F(self)/m
        v += 0.5*(a+a_new)*dt

        self.position = r / constants.units.L
        self.velocity = v * constants.units.T / constants.units.L