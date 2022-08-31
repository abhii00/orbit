import numpy as np
import pygame as pyg
import constants

class Explorer:
    '''Class to hold a manoeuvreable spacecraft
    
    Parameters:
        mass (float): the mass of the object (in true units)
        radius (float): the radius of the object (in true units)
        color (tuple): the color of the object
        position (np array): 2d vector of the position of the object (in true units)
        velocity (np array): 2d vector of the velocity of the object (in true units)
        orientation(np array): 2d vector of the orientation of the object
        trail_length (int): how many points to plot for the trail
    Returns:
        None
    '''

    def __init__(self, mass, radius, color, position, velocity, orientation, **kwargs):
        #init
        self.mass = mass
        self.radius = radius
        self.color = color
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.orientation = np.array(orientation, dtype='float64')
        self.trail_length = kwargs.get("trail_length", 1200)
        self.acceleration = np.empty_like(position, dtype='float64')
        self.trail = np.array([self.position, self.position])
        self.trail_color = tuple([val * 0.7 for val in self.color])
        self.trail_thickness = 1
    
    def draw(self, window):
        '''Draws the explorer onto a window.
        
        Parameters:
            window (pygame.display): the window onto which the body is drawn
        Returns:
            None
        '''

        pyg.draw.circle(window, self.color, self.position / constants.units.L, constants.disp.R(self.radius / constants.units.L))

        pyg.draw.lines(window, self.trail_color, False, (self.trail / constants.units.L).tolist(), self.trail_thickness)

    def move(self, F, timeStep):
        '''Updates the position and motion of the explorer.

        Parameters:
            F (np array): 2d vector of the forces on the body (in true units)
            timeStep (float): the time step size (in true units)
        '''
        m = self.mass
        a = F(self)/m
        v = self.velocity
        r = self.position
        dt = timeStep

        r += v*dt + 0.5*a*dt**2
        a_new = F(self)/m
        v += 0.5*(a+a_new)*dt

        self.position = r
        self.velocity = v

        self.trail = np.vstack([self.trail, self.position])
        if len(self.trail) > self.trail_length: self.trail = np.delete(self.trail, 0, 0)