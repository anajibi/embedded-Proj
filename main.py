import pygame
import math
from Color import *
from Tank import Tank

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Tank Game")

# Define colors


# Define tank properties
TANK_WIDTH = 50
TANK_HEIGHT = 30
TANK_SPEED = 5
TANK_TURN_SPEED = 3
TANK_HEALTH = 100

# Define bullet properties
BULLET_RADIUS = 5
BULLET_SPEED = 10

tank1 = Tank("tank2.png", 100, HEIGHT - TANK_HEIGHT // 2, 45)
tank2 = Tank("tank1.png", WIDTH - 100, HEIGHT - TANK_HEIGHT // 2, -45)



def generate_ground():
    ground_points = []
    amplitude = HEIGHT // 4  # Amplitude of the cosine wave
    frequency = 2  # Frequency of the cosine wave

    for x in range(0, WIDTH + 1):
        y = int(HEIGHT * 0.75 + amplitude * (
                math.cos(math.radians(x / WIDTH * 360 * frequency))
                +
                math.sin(math.radians(x / WIDTH * 360 * 2 / 3 * frequency)))
                )
        y = min(600, y)
        ground_points.append((x, y))

    return ground_points


# Load bullet image
bullet_image = pygame.Surface((BULLET_RADIUS * 2, BULLET_RADIUS * 2))
pygame.draw.circle(bullet_image, RED, (BULLET_RADIUS, BULLET_RADIUS), BULLET_RADIUS)

# Generate the ground
ground_points = generate_ground()

# Initialize bullet variables
bullet_x = 0
bullet_y = 0
bullet_dx = 0
bullet_dy = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # Limit the frame rate to 60 FPS

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys currently being pressed
    keys = pygame.key.get_pressed()

    # Tank 1 controls
    if keys[pygame.K_a]:
        tank1.angle += TANK_TURN_SPEED
    if keys[pygame.K_d]:
        tank1.angle -= TANK_TURN_SPEED
    if keys[pygame.K_w]:
        tank1.x += math.cos(math.radians(tank1.angle)) * TANK_SPEED
        tank1.y -= math.sin(math.radians(tank1.angle)) * TANK_SPEED
        # Keep tank 1 within the boundaries of the ground
        tank1.x = max(0, min(WIDTH, tank1.x))
        tank1.y = max(ground_points[int(tank1.x)][1], tank1.y)
        tank1.y = min(ground_points[int(tank1.x)][1] + TANK_HEIGHT // 2, tank1.y)
    if keys[pygame.K_SPACE]:
        # Shoot bullet from tank 1
        bullet_x = tank1.x + math.cos(math.radians(tank1.angle)) * (TANK_WIDTH // 2)
        bullet_y = tank1.y - math.sin(math.radians(tank1.angle)) * (TANK_WIDTH // 2)
        bullet_dx = math.cos(math.radians(tank1.angle)) * BULLET_SPEED
        bullet_dy = -math.sin(math.radians(tank1.angle)) * BULLET_SPEED

    # Tank 2 controls
    if keys[pygame.K_LEFT]:
        tank2.angle += TANK_TURN_SPEED
    if keys[pygame.K_RIGHT]:
        tank2.angle -= TANK_TURN_SPEED
    if keys[pygame.K_UP]:
        tank2.x += math.cos(math.radians(tank2.angle)) * TANK_SPEED
        tank2.y -= math.sin(math.radians(tank2.angle)) * TANK_SPEED
        # Keep tank 2 within the boundaries of the ground
        tank2.x = max(0, min(WIDTH, tank2.x))
        tank2.y = max(ground_points[int(tank2.x)][1], tank2.y)
        tank2.y = min(ground_points[int(tank2.x)][1] + TANK_HEIGHT // 2, tank2.y)
    if keys[pygame.K_RETURN]:
        # Shoot bullet from tank 2
        bullet_x = tank2.x + math.cos(math.radians(tank2.angle)) * (TANK_WIDTH // 2)
        bullet_y = tank2.y - math.sin(math.radians(tank2.angle)) * (TANK_WIDTH // 2)
        bullet_dx = math.cos(math.radians(tank2.angle)) * BULLET_SPEED
        bullet_dy = -math.sin(math.radians(tank2.angle)) * BULLET_SPEED

    # Move the bullet
    bullet_x += bullet_dx
    bullet_y += bullet_dy

    # Draw the background
    window.fill(BLACK)

    # Draw the ground
    pygame.draw.polygon(window, GREEN, ground_points)

    # Draw the tanks
    tank1.draw(window)
    tank2.draw(window)

    # Draw the bullets
    pygame.draw.circle(window, RED, (int(bullet_x), int(bullet_y)), BULLET_RADIUS)

    # Update the display
    pygame.display.flip()

pygame.quit()
