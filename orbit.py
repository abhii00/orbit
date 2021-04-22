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

        G = 1
        r = ao2.position - ao1.position
        return (G*ao1.mass*ao2.mass/np.linalg.norm(r)**2) * (r/np.linalg.norm(r))

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
            ao.velocity += self.dt*ao.acceleration
            ao.position += self.dt*ao.velocity

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

            #iterate through all the objects
            for i, ao in enumerate(self.astro_objects):
                #copy the list of objects and remove the current one
                astro_objects_temp = self.astro_objects.copy()
                astro_objects_temp.pop(i)

                #for every other object, calculate the acceleration
                #THIS IS INEFFICIENT AS FORCES ARE SYMMETRICAL
                for ao2 in astro_objects_temp:
                    ao.acceleration += self.gravitational_Force(ao, ao2)/ao.mass

                #numerically integrate to find new motion
                ao = self.numerical_Integrator("Euler", ao)

                #draw the object
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
        self.position = np.array(position, dtype="float64")
        self.velocity = np.array(velocity, dtype="float64")
        self.acceleration = np.empty_like(position, dtype="float64")

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
        astro_Object("1", (255,255,255), 1, 10, [200,300], [0,-1]),
        astro_Object("2", (255,255,255), 1, 10, [400,300], [0,1])
    ]
    universe = Universe(height=600, width=600, dt= 0.01, t_end=1000, astro_objects=aos)
    universe.start_Simulation()