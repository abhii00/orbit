import numpy as np
import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
pygame.init()

class Universe:
    """class to hold the plottable universe.
    
    Parameters:
        height (int): the pixel height of the window
        width (int): the pixel width of the window
        dt (float): the time increment
        t_end (float): the time to simulate until
        astro_objects (list): a list of the bodies in the universe
        
        starrysky_number (int): the number of stars in the starry background
        starrysky_twinklestep (int): the number of timesteps inbetween the background twinkles
        collision_detection_method (str): the collision detection method to use - pairwise, grid
        collision_method (str): the collision method to use - elastic, absorb
        collision_min_sep (float): the minimum percentage separation possible between objects + 1
        integration_method (str): the numerical integration method to use - Euler, Velocity Verlet
    Returns:
        None
    """

    def __init__(self, height, width, dt, t_end, astro_objects, **kwargs):
        """initialisation."""

        self.height = height
        self.width = width
        self.dt = dt
        self.t_end = t_end
        self.astro_objects = np.array(astro_objects)
        self.starrysky_number = kwargs.get("starrysky_number", 80)
        self.starrysky_twinklestep = kwargs.get("starrysky_twinklestep", 70)
        self.collision_detection_method = kwargs.get("collision_detection_method", "pairwise")
        self.collision_method = kwargs.get("collision_method", "absorb")
        self.collision_min_sep = kwargs.get("collision_min_sep", 1.001)
        self.integration_method = kwargs.get("integration_method", "Velocity Verlet")

        self.initialise_Background()
        
    def initialise_Background(self):
        """initialises the background."""

        #initialise window
        self.window = pygame.display.set_mode([self.height, self.width], pygame.DOUBLEBUF, 32)
        
        #randomly generate starry background
        self.starrysky = np.random.uniform(low=0,high=[self.width,self.height],size=(self.starrysky_number,2))
        
    def draw_Background(self):
        """draws the background."""

        #fill the screen black
        self.window.fill((0,0,0))

        #fill the screen with noise

        #generate random intensities for twinkling
        if (self.step % self.starrysky_twinklestep == 0):
            self.starrysky_colors = [np.random.uniform(low=200, high=255) for starrystar in self.starrysky]
            self.starrysky_radii = np.random.randint(low=1,high=3,size=self.starrysky_number)

        #draw starrysky
        for i, starrystar in enumerate(self.starrysky):
            starrystar_color = self.starrysky_colors[i]
            starrystar_radius = self.starrysky_radii[i]
            pygame.draw.circle(self.window, (starrystar_color,starrystar_color,starrystar_color), starrystar, starrystar_radius)

    def create_Objectbymouse(self):
        """adds objects using the mouse."""
        #id
        ID = str(np.shape(self.astro_objects)[0])

        #color
        color = tuple(np.random.uniform(low=0, high=255, size=3))

        #mass
        mass = 0.01

        #radius
        radius = 2

        #position
        position = [x for x in pygame.mouse.get_pos()]

        #velocity
        velocity = [0,0]
        
        #create object
        ao = astro_Object(ID, color,mass, radius, position, velocity)
        self.astro_objects = np.append(self.astro_objects, ao)

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

    def collide_Objects(self, detection_method, collision_method):
        """detects and handles collisions between objects.
        
        Parameters:
            detection_method (str): collision detection method - pairwise, grid
            collision_method (str): collision method - elastic, absorb
        Returns:
            None
        """

        def collide_Pairwise(aos, collision_method):
            """handles pairwise collision between objects.

            Parameters:
                aos (list): list of pairs of objects to collide
                collision_method (str): collision method - elastic, absorb
            Returns:
                None
            """
            colliding_objects = []

            #check if objects actually colliding
            for i, ao1 in enumerate(aos):
                for j, ao2 in enumerate(aos):

                    if not(i == j or (j, i) in colliding_objects):
                        r = np.linalg.norm(ao1.position - ao2.position)
                        minsep = ao1.radius + ao2.radius
                        minsep *= self.collision_min_sep

                        if r <= minsep:
                            colliding_objects.append((i,j))
            
            #elastic collisions
            if collision_method == "elastic":
                for pair in colliding_objects:
                    ao1 = self.astro_objects[pair[0]]
                    ao2 = self.astro_objects[pair[1]]

                    u1 = ao1.velocity
                    u2 = ao2.velocity

                    total_mass = ao1.mass + ao2.mass

                    #conservation of momentum and energy
                    ao1.velocity = (u1*(ao1.mass - ao2.mass) + u2*2*ao2.mass)/total_mass
                    ao2.velocity = (u1*(ao2.mass - ao1.mass) + u2*2*ao1.mass)/total_mass

                    self.astro_objects[pair[0]] = ao1
                    self.astro_objects[pair[1]] = ao2
            
            #absorption collision
            elif collision_method == "absorb":
                aos_to_add = np.array([])
                aos_to_delete = []

                for pair in colliding_objects:
                    ao1 = self.astro_objects[pair[0]]
                    ao2 = self.astro_objects[pair[1]]

                    #id
                    ID = "Col. between {} and {}".format(ao1.ID, ao2.ID)

                    #average colour
                    weighted_ao1_color = tuple([val*ao1.mass for val in ao1.color])
                    weighted_ao2_color = tuple([val*ao2.mass for val in ao2.color])
                    weighted_colors = (weighted_ao1_color, weighted_ao2_color)
                    temp_color = [sum(y) / len(y) for y in zip(*weighted_colors)]
                    color = tuple([255*x/max(temp_color) for x in temp_color])

                    #total mass
                    mass = ao1.mass + ao2.mass

                    #radius
                    radius = np.cbrt(ao1.radius**3 + ao2.radius**3)

                    #position
                    if ao1.mass > ao2.mass:
                        position = ao1.position
                    else:
                        position = ao2.position

                    #velocity
                    velocity = (ao1.mass*ao1.velocity + ao2.mass*ao2.velocity)/mass
                    print(ao1.velocity)
                    print(ao2.velocity)
                    print(velocity)

                    #create new object
                    ao = astro_Object(ID, color, mass, radius, position, velocity)
                    ao.atmos_proportion = ((ao1.radius**3)*ao1.atmos_proportion + (ao2.radius**3)*ao2.atmos_proportion)/(2*(ao.radius**3))
                    aos_to_add = np.append(aos_to_add, ao)

                    #queue old objects to be deleted
                    aos_to_delete.append(pair[0])
                    aos_to_delete.append(pair[1])
                
                if np.any(aos_to_add):
                    #delete old objects
                    self.astro_objects = np.delete(self.astro_objects, aos_to_delete)

                    #add new objects
                    self.astro_objects = np.append(self.astro_objects, aos_to_add)

        #check for colliding objects if seperation small enough
        if detection_method == "pairwise":
            collide_Pairwise(self.astro_objects, self.collision_method)
        
        #returns a set of coords for each box in a 2 by 2 grid and then checks if colliding
        elif detection_method == "grid":
            
            boxes = [[], [], [], []]
            for i, ao in enumerate(self.astro_objects):
                x = ao.position[0]
                y = ao.position[1]
                if x <= self.width/2 and y <= self.height/2:
                    boxes[0].append(i)
                elif x > self.width/2 and y <= self.height/2:
                    boxes[1].append(i)
                elif x > self.width/2 and y > self.height/2:
                    boxes[2].append(i)
                else:
                    boxes[3].append(i)
            
            for box in boxes:
                if len(box) > 1:
                    collide_Pairwise(self.astro_objects[box], self.collision_method)

    def start_Simulation(self, test=False):
        """simulates the motion."""

        self.sim_run = True
        self.t = 0
        self.step = 0
        
        #main loop
        while self.sim_run:
            
            #check events
            for event in pygame.event.get():
                #break out of loop if window exited
                if event.type == pygame.QUIT:
                    self.sim_run = False
                #add object if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.create_Objectbymouse()

            #break out of loop if maximum time reached
            if self.t > self.t_end: 
                self.sim_run = False

            #draw the background
            self.draw_Background()

            #save positions of objects
            self.astro_objects_original = self.astro_objects.copy()

            #iterate through all the objects
            self.collide_Objects(self.collision_detection_method, self.collision_method)
            for i, ao in enumerate(self.astro_objects):
                #numerically integrate to find new motion
                ao.update_Motion(self.integration_method, self.gravitational_Field, self.dt)

                #draw the object
                ao.draw_Object(self.window)
                ao.draw_Trail(self.window)

            #update window
            self.step += 1
            self.t += self.dt
            pygame.display.flip()

            #end simulation after one loop if testing
            if test: self.sim_run = False

class astro_Object:
    """class to hold a single star/planet/moon.
    
    Parameters:
        ID (str): a distinguishable ID for the object
        color (tuple): the color of the object
        mass (float): the mass of the object
        radius (float): the radius of the object
        position (list): the position of the object
        velocity (list): the velocity of the object

        min_trail_length (int): the minimum length of the trail
        trail_length (int): the length of the trail
    Returns:
        None
    
    """
    def __init__(self, ID, color, mass, radius, position, velocity, **kwargs):
        """initialisation."""

        self.ID = ID
        self.color = color
        self.mass = mass
        self.radius = radius

        self.position = np.array(position, dtype="float64")
        self.velocity = np.array(velocity, dtype="float64")
        self.acceleration = np.empty_like(position, dtype="float64")

        self.min_trail_length = kwargs.get("min_trail_length", 10)
        self.trail_length = kwargs.get("trail_length", 1000)

        self.trail = [list(self.position)]
        self.trail_color = tuple([val * 0.7 for val in self.color])
        self.trail_thickness = int(np.floor(0.2*self.radius)) + 1

        self.atmos_color = tuple([val * 0.3 for val in self.color])
        self.atmos_proportion = np.random.uniform(low = 0.5, high = 1)
    
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

        if np.linalg.norm(self.position - self.trail[-1]) > 0.01:
            self.trail.append(list(self.position))
            
    def draw_Object(self, window):
        """draws the object on a given window.
        
        Parameters:
            window (pygame.display): the window on which to draw the body onto
        Returns:
            None
        """

        #draw atmosphere
        pygame.draw.circle(window, self.atmos_color, self.position, self.radius)

        #draw object
        pygame.draw.circle(window, self.color, self.position, self.radius*self.atmos_proportion)

    def draw_Trail(self, window):
        """draws the object trail.

        Parameters:
            window (pygame.display): the window on which to draw the trail onto
        Returns:
            None
        """
        
        #check if trail long enough
        if len(self.trail) > self.min_trail_length:

            #check if trail shorter than expected length and draw whole length
            if len(self.trail) < self.trail_length:
                pygame.draw.lines(window, self.trail_color, False, self.trail, self.trail_thickness)
            #draw first trail_length points
            else:
                pygame.draw.lines(window, self.trail_color, False, self.trail[len(self.trail) - self.trail_length:], self.trail_thickness)

if __name__ =="__main__":
    aos = [
        astro_Object("1", (255,255,255), 10, 15, [400,400], [0,0]),
        astro_Object("2", (255,0,255), 0.1, 3, [200,400], [0, 5]),
        astro_Object("3", (0,255,255), 0.1, 3, [600,400], [0, -5]),
        astro_Object("4", (255,255,0), 0.1, 3, [400,200], [-5, 0]),
        astro_Object("5", (200,50,0), 0.1, 3, [400,600], [5, 0])
    ]
    universe = Universe(height=800, width=800, dt=0.5, t_end=2000, astro_objects=aos)
    universe.start_Simulation()