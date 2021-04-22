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
        
        starrysky_size (int): the number of stars in the starry background
        starrysky_twinklestep (int): the number of timesteps inbetween the background twinkles
    Returns:
        None
    """

    def __init__(self, height, width, dt, t_end, astro_objects, **kwargs):
        """initialisation."""

        self.height = height
        self.width = width
        self.dt = dt
        self.t_end = t_end
        self.astro_objects = astro_objects
        self.starrysky_size = kwargs.get("starrysky_size", 80)
        self.starrysky_twinklestep = kwargs.get("starrysky_twinklestep", 70)

        self.initialise_Background()
        
    def initialise_Background(self):
        """initialises the background."""

        #initialise window
        self.window = pygame.display.set_mode([self.height, self.width])

        #randomly generate starry background
        self.starrysky = np.random.uniform(low=0,high=[self.width,self.height],size=(self.starrysky_size,2))
        
    def draw_Background(self):
        """draws the background."""

        #fill the screen black
        self.window.fill((0,0,0))

        #generate random intensities for twinkling
        if (self.step % self.starrysky_twinklestep == 0):
            self.starrysky_colors = [np.random.uniform(low=200, high=255) for starrystar in self.starrysky]
            self.starrysky_radii = np.random.randint(low=1,high=3,size=self.starrysky_size)

        #draw starrysky
        for i, starrystar in enumerate(self.starrysky):
            starrystar_color = self.starrysky_colors[i]
            starrystar_radius = self.starrysky_radii[i]
            pygame.draw.circle(self.window, (starrystar_color,starrystar_color,starrystar_color), starrystar, starrystar_radius)

    def gravitational_Field(self, x):
        """calculates the gravitational field at a given point in space.
        
        Parameters:
            x (list): position
        Returns:
            A list containing the force vector.
        """

        G = 1000
        
        g = 0
        for ao in self.astro_objects_original:
            r = ao.position - x
            if np.linalg.norm(r) > 0.01:
                g += (G*ao.mass/np.linalg.norm(r)**2) * (r/np.linalg.norm(r))

        return g

    def start_Simulation(self):
        """simulates the motion."""

        self.sim_run = True
        self.t = 0
        self.step = 0
        
        #main loop
        while self.sim_run:
            #break out of loop if window exited
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sim_run = False

            #break out of loop if maximum time reached
            if self.t > self.t_end: 
                self.sim_run = False

            #draw the background
            self.draw_Background()

            #save positions of objects
            self.astro_objects_original = self.astro_objects.copy()

            #iterate through all the objects
            for i, ao in enumerate(self.astro_objects):
                #numerically integrate to find new motion
                ao.update_Motion("Velocity Verlet", self.gravitational_Field, self.dt)
                ao.update_Trail()

                #draw the object
                ao.draw_Object(self.window)
                ao.draw_Trail(self.window)

            #update window
            self.step += 1
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
        self.trail = []
        self.velocity = np.array(velocity, dtype="float64")
        self.acceleration = np.empty_like(position, dtype="float64")
    
    def update_Motion(self, method, acc, dt):
        """numerically integrates the motion.

        Parameters:
            method (str): the numerical integrator to use - Euler, Velocity Verlet
            acc (func): a function returning acceleration as a function of position
        Returns:
            None
        """
        
        #euler
        if method == "Euler":
            self.acceleration = acc(self.position)

            self.position += self.velocity*dt

            self.velocity += self.acceleration*dt

        #velocity verlet
        elif method == "Velocity Verlet":
            self.acceleration = acc(self.position)

            self.position += self.velocity*dt + 0.5*self.acceleration*(dt**2)

            self.velocity += 0.5*(self.acceleration+acc(self.position))*dt

    def update_Trail(self, trail_length = 3000):
        """updates the object's trail"""

        self.trail.append(list(self.position))

        if len(self.trail) > trail_length:
            del self.trail[0]
            
    def draw_Object(self, window):
        """draws the object on a given window.
        
        Parameters:
            window (pygame.display): the window on which to draw the body onto
        Returns:
            None
        """

        pygame.draw.circle(window, self.color, self.position, self.radius)
        
    def draw_Trail(self, window, min_trail_length = 5):
        """draws the object trail.

        Parameters:
            window (pygame.display): the window on which to draw the trail onto
        Returns:
            None
        """

        if len(self.trail) > min_trail_length:
            pygame.draw.lines(window, self.color, False, self.trail, 2)

if __name__ =="__main__":
    aos = [
        astro_Object("1", (0,0,255), 10, 10, [200,300], [2,-2]),
        astro_Object("2", (255,0,0), 10, 10, [400,300], [-2,2]),
        astro_Object("3", (0,255,0), 10, 7, [700,400], [-2,2]),
        astro_Object("bigchonker", (255,255,255), 100, 30, [500,500], [0,0])
    ]
    universe = Universe(height=800, width=800, dt= 0.01, t_end=1000, astro_objects=aos)
    universe.start_Simulation()