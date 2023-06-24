import pygame

import Color


class Bullet:
    color = Color.RED

    intensity = 5

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
