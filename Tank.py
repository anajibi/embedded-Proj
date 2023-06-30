import math

import pygame

from Bullet import Bullet
from Color import RED, GREEN
from Config import *


class Tank:
    image_path: str
    image: pygame.Surface
    x: int
    y: int

    angle: float
    speed: float

    health: int

    def __init__(self, image_path: str, x: int, y: int, angle: float, ground_points: list):
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TANK_DIM, TANK_DIM))
        self.x = x
        self.y = y
        self.angle = angle

        self.health = 100

        self.ground_points = ground_points

    def rotate(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(center=(self.x, self.y)).center)
        return rotated_image, new_rect

    def draw_health_bar(self, win: pygame.Surface):
        health_bar = pygame.Rect(self.x - TANK_WIDTH // 2, self.y - TANK_HEIGHT, TANK_WIDTH, 5)

        health_percentage = self.health / TANK_HEALTH
        health_width = int(health_percentage * TANK_WIDTH)

        pygame.draw.rect(win, RED, health_bar)  # Full health bar
        pygame.draw.rect(win, GREEN,
                         (health_bar.left, health_bar.top, health_width, health_bar.height))

    def draw(self, win: pygame.Surface):
        self.draw_health_bar(win)

        rotated_image, rect = self.rotate(self.angle)
        win.blit(rotated_image, rect.topleft)

    def move(self, amount):
        self.x += amount
        self.y -= amount
        # Keep tank 2 within the boundaries of the ground
        self.x = max(0, min(GAME_WIDTH, self.x))
        self.y = max(self.ground_points[int(self.x)][1], self.y)
        self.y = min(self.ground_points[int(self.x)][1] + TANK_HEIGHT // 2, self.y)

    def left(self):
        self.move(-TANK_SPEED)

    def right(self):
        self.move(+TANK_SPEED)

    def check_hit(self, bullet: Bullet):
        if self.x - TANK_WIDTH // 2 - BULLET_RADIUS < bullet.hit_x < self.x + TANK_WIDTH // 2 + BULLET_RADIUS \
                and self.y - TANK_HEIGHT - BULLET_RADIUS < bullet.hit_y < self.y + BULLET_RADIUS:
            self.health -= BULLET_WEIGHT
            return True
        return False
