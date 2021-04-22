import numpy as np
import pygame

class Universe:
    """class to hold the plottable universe.
    
    Parameters:
        height (int): the pixel height of the window
        width (int): the pixel width of the window
        dt (float): the time increment
        t_end (float): the time to simulate until
        astro_objects (list): a list of the bodies in the universe
    Returns:
        None
    """

    def __init__(self, height, width, dt, t_end, astro_objects):
        """initialisation."""

        self.height = height
        self.width = width
        self.dt = dt
        self.t_end = t_end
        self.window = pygame.display.set_mode([self.height, self.width])
        self.astro_objects = astro_objects

    def gravitational_Force(self, ao1, ao2):
        """calculates the gravitational attraction between a pair of objects.
        
        Parameters:
            ao1 (astro_Object): the first object
            ao2 (astro_Object): the second object
        Returns:
            A list containing the force vector.
        """
        pass

    def numerical_Integrator(self, method, ao):
        """numerically integrates the motion for a single object.

        Parameters:
            method (str): the numerical integrator to use - Euler
            ao (astro_Object): the object
        Returns:
            A new astro_Object with new position/velocity/acceleration
        """
        
        #euler integration
        if method == "Euler":
            ao.position = [x + self.dt*ao.velocity[i] for i,x in enumerate(ao.position)]

        return ao

    def start_Simulation(self):
        """simulates the motion."""

        self.sim_run = True
        self.t = 0
        
        #main loop
        while self.sim_run:
            #break out of loop if window exited
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sim_run = False

            #break out of loop if maximum time reached
            if self.t > self.t_end: 
                self.sim_run = False

            #fill the screen black
            self.window.fill((0,0,0))

            #iterate through all the bodies
            for ao in self.astro_objects:
                #numerically integrate to find new motion
                self.numerical_Integrator("Euler",ao)

                #draw all the bodies
                ao.draw_Object(self.window)

            #update window
            self.t += self.dt
            pygame.display.flip()

class astro_Object:
    """class to hold a single star/planet/moon.
    
    Parameters:
        ID (str): a distinguishable ID for the object
        color (tuple): the color of the object
        mass (float): the mass of the object
        radius (float): the radius of the object
        position (list): the position of the object
        velocity (list): the velocity of the object
    Returns:
        None
    
    """
    def __init__(self, ID, color, mass, radius, position, velocity):
        """initialisation."""

        self.ID = ID
        self.color = color
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.acceleration = 0

    def draw_Object(self, window):
        """draws the object on a given window.
        
        Parameters:
            window (pygame.display): the window on which to draw the body onto
        Returns:
            None
        """

        pygame.draw.circle(window, self.color, self.position, self.radius)

if __name__ =="__main__":
    aos = [
        astro_Object("1", (255,255,255), 1, 10, [300,300], [1,1]),
        astro_Object("1", (255,0,0), 1, 10, [300,300], [1,1])
    ]
    universe = Universe(height=600, width=600, dt= 0.01, t_end=100, astro_objects=aos)
    universe.start_Simulation()