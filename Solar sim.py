import pygame
import math
pygame.init()


WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar sim")
YELLOW = (255, 255, 0)


class Planet:
    au = 149.6e6 * 1000
    G = 6.67408e-11
    SCALE = 250/au
    TIMESTEP = 3600*24

    def __init__(self, x, y, rad, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.rad = rad
        self.color = color

        self.orbit = []
        self.sun = False
        self.distance_from_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x*self.SCALE + WIDTH/2
        y = self.y*self.SCALE + HEIGHT/2
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.rad)


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, 1.98892*10**30, YELLOW)
    sun.sun = True

    planets = [sun]
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WINDOW)

        pygame.display.update()
    pygame.quit()


main()
