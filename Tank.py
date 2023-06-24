import math

import pygame

TANK_DIM = 65

class Tank:

    image_path: str
    image: pygame.Surface
    x: int
    y: int

    angle: float
    speed: float

    health: int
    def __init__(self, image_path: str, x: int, y: int, angle: float):
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TANK_DIM, TANK_DIM))
        self.x = x
        self.y = y
        self.angle = angle

        self.health = 100

    def rotate(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(center=(self.x, self.y)).center)
        return rotated_image, new_rect

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self, win: pygame.Surface):
        rotated_image, rect = self.rotate(self.angle)
        win.blit(rotated_image, rect.topleft)

