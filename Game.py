import math
from enum import Enum
from typing import List

import pygame

from AimIndicator import AimIndicator
from Bullet import Bullet
from Color import BLACK, GREEN, YELLOW, RED
from Config import GAME_WIDTH, GAME_HEIGHT, FPS
from SoundDetector import SoundDetector
from SpeedDetector import SpeedDetector
from Tank import Tank, TANK_HEIGHT


class GameState(Enum):
    CHOOSE_ANGLE = 0
    CHOOSE_POWER = 1
    SHOOT = 2


class Game:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("Two-Player Tank Game")

        self.sound_detector = SoundDetector()
        self.speed_detector = SpeedDetector()
        self.generate_ground()

    def generate_ground(self):
        ground_points = []
        amplitude = GAME_HEIGHT // 4  # Amplitude of the cosine wave
        frequency = 2  # Frequency of the cosine wave

        for x in range(0, GAME_WIDTH + 1):
            y = int(GAME_HEIGHT * 0.75 + amplitude * (
                    math.cos(math.radians(x / GAME_WIDTH * 360 * frequency))
                    +
                    math.sin(math.radians(x / GAME_WIDTH * 360 * 2 / 3 * frequency)))
                    )
            y = min(GAME_HEIGHT, y)
            ground_points.append((x, y))

        self.ground_points = ground_points

    def run(self):
        running = True
        clock = pygame.time.Clock()

        turn = 0
        turn_array: List[Tank] = [
            Tank("./tank2.bmp", 100, GAME_HEIGHT - TANK_HEIGHT // 2, 45, self.ground_points),
            Tank("./tank1.bmp", GAME_WIDTH - 100, GAME_HEIGHT - TANK_HEIGHT // 2, -45, self.ground_points)
        ]

        state = GameState.CHOOSE_ANGLE
        aim_indicator = AimIndicator(turn_array[turn])

        bullet = None

        self.sound_detector.turn_on()

        while running:
            clock.tick(FPS)

            self.window.fill(BLACK)
            pygame.draw.polygon(self.window, GREEN, self.ground_points)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            if state == GameState.CHOOSE_ANGLE or state == GameState.CHOOSE_POWER:
                if keys[pygame.K_LEFT]:
                    turn_array[turn].left()
                if keys[pygame.K_RIGHT]:
                    turn_array[turn].right()

            if state == GameState.CHOOSE_ANGLE:
                if self.sound_detector.is_sound_detected():
                    self.sound_detector.turn_off()
                    self.speed_detector.turn_on()
                    state = GameState.CHOOSE_POWER

                aim_indicator.indicate(self.window)

            elif state == GameState.CHOOSE_POWER:
                if self.speed_detector.is_speed_detected():
                    bullet = Bullet(turn_array[turn].x, turn_array[turn].y,
                                    aim_indicator.get_shoot_angle(),
                                    self.speed_detector.detected_speed,
                                    self.ground_points)
                    self.speed_detector.turn_off()
                    state = GameState.SHOOT
                aim_indicator.draw(self.window)

            elif state == GameState.SHOOT:
                if bullet.hit:
                    turn = (turn + 1) % 2
                    self.sound_detector.turn_on()
                    aim_indicator = AimIndicator(turn_array[turn])
                    turn_array[turn].check_hit(bullet)
                    state = GameState.CHOOSE_ANGLE

                else:
                    bullet.fire(self.window)
                    self.indicate_power(bullet.power)

            for tank in turn_array:
                tank.draw(self.window)

            pygame.display.flip()

    def indicate_power(self, power):
        power_percentage = int(
            power) % 101  # Calculate power as a percentage

        # Calculate the height of the color bar based on the power percentage
        color_bar_height = int(power_percentage / 100 * GAME_HEIGHT)

        # Calculate the colors at the top and bottom of the color bar
        if power_percentage <= 50:
            # Yellow to green transition
            yellow = pygame.Color("yellow")
            green = pygame.Color("green")
            top_color = yellow.lerp(green, power_percentage / 100)
            bottom_color = yellow.lerp(green, (power_percentage + 1) / 100)
        else:
            # Green to red transition
            green = pygame.Color("green")
            red = pygame.Color("red")
            top_color = green.lerp(red, (power_percentage - 20) / 100)
            bottom_color = green.lerp(red, (power_percentage - 19) / 100)

        # Draw the color bar
        pygame.draw.rect(self.window, top_color, (10, GAME_HEIGHT - color_bar_height, 20, color_bar_height))
        pygame.draw.rect(self.window, bottom_color, (10, GAME_HEIGHT - color_bar_height - 1, 20, 1))
