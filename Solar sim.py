import pygame
import math
pygame.init()


WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar sim")
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
GREY = (80, 78, 81)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    au = 149.6e6 * 1000
    G = 6.67408e-11
    SCALE = 200/au
    TIMESTEP = 3600*24

    def __init__(self, x, y, rad, mass, color):
        self.x = x  # x position
        self.y = y  # y position
        self.mass = mass    # mass
        self.rad = rad  # radius
        self.color = color  # color

        self.orbit = []
        self.sun = False
        self.distance_from_sun = 0  # distance from sun

        self.x_vel = 0  # x velocity
        self.y_vel = 0  # y velocity

    def draw(self, win):
        x = self.x*self.SCALE + WIDTH/2  # x position on screen
        y = self.y*self.SCALE + HEIGHT/2    # y position on screen

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x*self.SCALE + WIDTH/2
                y = y*self.SCALE + HEIGHT/2
                updated_points.append((x, y))  # x, y position on screen
            pygame.draw.lines(WINDOW, self.color, False,
                              updated_points, 2)  # draw orbit

        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun/1000 ,1 )}km", 1, WHITE)
            WINDOW.blit(distance_text, (x, y))  # draw distance text
        pygame.draw.circle(win, self.color, (int(x), int(y)),
                           self.rad)  # draw the planets

    def grav(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / \
            distance**2   # force = G * m1 * m2 / r^2
        # angle between the two planets
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force   # force in x direction
        force_y = math.sin(theta) * force   # force in y direction
        return force_x, force_y  # return the force in x and y directions

    def position(self, planets):
        total_fx = total_fy = 0     # total force in x and y directions
        for planet in planets:  # loop through all planets
            if self == planet:
                continue
            fx, fy = self.grav(planet)  # get the force in x and y directions
            total_fx += fx      # add the force to the total force in x direction
            total_fy += fy    # add the force to the total force in y direction
        # update the velocity in x direction
        self.x_vel += total_fx / self.mass*self.TIMESTEP
        # update the velocity in y direction
        self.y_vel += total_fy / self.mass*self.TIMESTEP
        self.x += self.x_vel*self.TIMESTEP  # update the position in x direction
        self.y += self.y_vel*self.TIMESTEP  # update the position in y direction
        # add the position to the orbit list
        self.orbit.append((self.x, self.y))


def main():
    run = True  # run the program
    clock = pygame.time.Clock()  # clock to keep track of time

    sun = Planet(0, 0, 30, 1.98892*10**30, YELLOW)  # create the sun
    sun.sun = True  # set the sun to true

    mercury = Planet(0.387 * Planet.au, 0, 8, 3.30 *
                     10**23, GREY)    # create mercury
    mercury.y_vel = 47.7*1000   # set the velocity of mercury in y direction

    venus = Planet(0.723 * Planet.au, 0, 14, 4.869 *
                   10**24, WHITE)   # create venus
    venus.y_vel = -35.02*1000   # set the velocity of venus in y direction

    earth = Planet(-1 * Planet.au, 0, 16, 5.9742*10**24, BLUE)  # create earth
    earth.y_vel = 29.783 * 1000  # set the velocity of earth in y direction

    mars = Planet(-1.524 * Planet.au, 0, 12, 6.39*10**23, RED)  # create mars
    mars.y_vel = 24.077 * 1000  # set the velocity of mars in y direction

    # create a list of all the planets
    planets = [sun, mercury, venus, earth, mars]
    while run:
        clock.tick(60)
        WINDOW.fill(BLACK)  # fill the window with black

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # if the user clicks the x button
                run = False  # stop the program

        for planet in planets:
            planet.position(planets)    # update the position of each planet
            planet.draw(WINDOW)  # draw the planets

        pygame.display.update()
    pygame.quit()


main()
