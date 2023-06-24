import pygame
import math

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Tank Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define tank properties
TANK_WIDTH = 50
TANK_HEIGHT = 30
TANK_SPEED = 5
TANK_TURN_SPEED = 3
TANK_HEALTH = 100

# Define bullet properties
BULLET_RADIUS = 5
BULLET_SPEED = 10

# Define the initial positions and directions of the tanks
tank1_x = 100
tank1_y = HEIGHT - TANK_HEIGHT // 2
tank1_angle = 45
tank2_x = WIDTH - 100
tank2_y = HEIGHT - TANK_HEIGHT // 2
tank2_angle = 135

# Define the initial health of the tanks
tank1_health = TANK_HEALTH
tank2_health = TANK_HEALTH

# Function to rotate an image around its center
def rotate(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(tank1_x, tank1_y)).center)
    return rotated_image, new_rect

# Load tank images
tank1_image = pygame.image.load("tank1.png")
tank1_image = pygame.transform.scale(tank1_image, (TANK_WIDTH, TANK_HEIGHT))
tank2_image = pygame.image.load("tank2.png")
tank2_image = pygame.transform.scale(tank2_image, (TANK_WIDTH, TANK_HEIGHT))

# Load bullet image
bullet_image = pygame.Surface((BULLET_RADIUS * 2, BULLET_RADIUS * 2))
pygame.draw.circle(bullet_image, RED, (BULLET_RADIUS, BULLET_RADIUS), BULLET_RADIUS)

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
        tank1_angle += TANK_TURN_SPEED
    if keys[pygame.K_d]:
        tank1_angle -= TANK_TURN_SPEED
    if keys[pygame.K_w]:
        tank1_x += math.cos(math.radians(tank1_angle)) * TANK_SPEED
        tank1_y -= math.sin(math.radians(tank1_angle)) * TANK_SPEED
    if keys[pygame.K_SPACE]:
        # Shoot bullet from tank 1
        bullet_x = tank1_x + math.cos(math.radians(tank1_angle)) * (TANK_WIDTH // 2)
        bullet_y = tank1_y - math.sin(math.radians(tank1_angle)) * (TANK_WIDTH // 2)
        bullet_dx = math.cos(math.radians(tank1_angle)) * BULLET_SPEED
        bullet_dy = -math.sin(math.radians(tank1_angle)) * BULLET_SPEED

    # Tank 2 controls
    if keys[pygame.K_LEFT]:
        tank2_angle += TANK_TURN_SPEED
    if keys[pygame.K_RIGHT]:
        tank2_angle -= TANK_TURN_SPEED
    if keys[pygame.K_UP]:
        tank2_x += math.cos(math.radians(tank2_angle)) * TANK_SPEED
        tank2_y -= math.sin(math.radians(tank2_angle)) * TANK_SPEED
    if keys[pygame.K_RETURN]:
        # Shoot bullet from tank 2
        bullet_x = tank2_x + math.cos(math.radians(tank2_angle)) * (TANK_WIDTH // 2)
        bullet_y = tank2_y - math.sin(math.radians(tank2_angle)) * (TANK_WIDTH // 2)
        bullet_dx = math.cos(math.radians(tank2_angle)) * BULLET_SPEED
        bullet_dy = -math.sin(math.radians(tank2_angle)) * BULLET_SPEED

    # Move the bullet
    bullet_x += bullet_dx
    bullet_y += bullet_dy

    # Draw the background
    window.fill(BLACK)

    # Draw the tanks
    tank1_image_rotated, tank1_rect = rotate(tank1_image, tank1_angle)
    tank2_image_rotated, tank2_rect = rotate(tank2_image, tank2_angle)
    window.blit(tank1_image_rotated, tank1_rect.topleft)
    window.blit(tank2_image_rotated, tank2_rect.topleft)

    # Draw the bullets
    pygame.draw.circle(window, RED, (int(bullet_x), int(bullet_y)), BULLET_RADIUS)

    # Update the display
    pygame.display.flip()

pygame.quit()
