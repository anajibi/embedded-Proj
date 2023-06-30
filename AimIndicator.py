import math

import numpy as np
import pygame

from Color import WHITE
from Config import DEFAULT_POWER, GRAVITY, AIM_TEMPO, DOTTED_LINE_SPACING, LINE_LENGTH
from Tank import TANK_WIDTH, Tank


class AimIndicator:
    angle: float
    tank: Tank

    def __init__(self, tank: Tank):
        self.angle = 0
        self.tank = tank

    def indicate(self, win: pygame.Surface):
        self.draw(win)

        self.angle += AIM_TEMPO
        self.angle %= 360

    def draw(self, win: pygame.Surface):
        temp_angle = 180 - math.fabs(self.angle - 180)
        line_start_x = self.tank.x + math.cos(math.radians(temp_angle)) * (TANK_WIDTH // 2)
        line_start_y = self.tank.y - math.sin(math.radians(temp_angle)) * (TANK_WIDTH // 2)

        current_x = line_start_x
        current_y = line_start_y

        while math.hypot(current_x - line_start_x, current_y - line_start_y) < LINE_LENGTH:
            pygame.draw.circle(win, WHITE, (int(current_x), int(current_y)), 2)
            current_x += math.cos(math.radians(temp_angle)) * DOTTED_LINE_SPACING
            current_y -= math.sin(math.radians(temp_angle)) * DOTTED_LINE_SPACING


    def get_shoot_angle(self):
        return 180 - math.fabs(self.angle - 180)