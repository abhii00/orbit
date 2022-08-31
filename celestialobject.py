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

    def __init__(self, mass, radius, color, position, velocity, **kwargs):
        #init
        self.mass = mass
        self.radius = radius
        self.color = color
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.min_trail_length = kwargs.get("min_trail_length", 10)
        self.trail_length = kwargs.get("trail_length", 1200)
        self.acceleration = np.empty_like(position, dtype='float64')
        self.trail = [list(self.position)]
        self.trail_color = tuple([val * 0.7 for val in self.color])
        self.trail_thickness = int(np.floor(0.2*self.radius)) + 1
    
    def draw(self, window):
        '''Draws the body onto a window.
        
        Parameters:
            window (pygame.display): the window onto which the body is drawn
        Returns:
            None
        '''

        pyg.draw.circle(window, self.color, self.position, self.radius*constants.disp.R)

        if len(self.trail) > self.min_trail_length:
            #check if trail shorter than expected length and draw whole length
            if len(self.trail) < self.trail_length:
                pyg.draw.lines(window, self.trail_color, False, self.trail, self.trail_thickness)
            #draw first trail_length points
            else:
                pyg.draw.lines(window, self.trail_color, False, self.trail[len(self.trail) - self.trail_length:], self.trail_thickness)

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

        if np.linalg.norm(self.position - self.trail[-1]) > 0.01:
            self.trail.append(list(self.position))