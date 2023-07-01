import math

import numpy as np
import pygame

import Color
from Config import BULLET_RADIUS, GRAVITY, GAME_WIDTH, FPS, GAME_HEIGHT


class Bullet:
    color = Color.RED

    angle: float
    power: float

    hit_x: float
    hit_y: float

    def __init__(self, x, y, angle, power, ground_points):
        self.x = x
        self.y = y

        self.angle = angle
        self.power = power

        self.ground_points = ground_points

        self.hit = False
        self.t = 0

    def draw(self, win, ):
        pygame.draw.circle(win, self.color, (self.hit_x, self.hit_y), BULLET_RADIUS)

    def _get_x(self, t):
        return self.x + math.cos(math.radians(self.angle)) * self.power * t

    def _get_y(self, t):
        return self.y - math.sin(math.radians(self.angle)) * self.power * t + GRAVITY * t * t / 2

    def move(self):
        if self.hit:
            return
        self.hit_x = int(self._get_x(self.t))
        self.hit_y = int(self._get_y(self.t))

        self.t += 0.2

        if self.hit_x > GAME_WIDTH or self.hit_x < 0 \
                or self.hit_y > GAME_HEIGHT or self.hit_y < 0:
            self.hit = True

        # if GAME_WIDTH > self.hit_x > 0:
        #     if self.hit_y > self.ground_points[self.hit_x][1]:
        #         self.hit_y = self.ground_points[self.hit_x][1]
        #         self.hit = True

    def fire(self, win):
        self.move()
        self.draw(win)
