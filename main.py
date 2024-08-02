import pygame
from plane import Plane

pygame.init()

# Create game window
screen_width = 1000
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("1v1 Plane Game")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

def draw_health_bar(health, screen, x, y):
    if health == 3:
        screen.blit(full_heart, (x, y))
        screen.blit(full_heart, (x + 30, y))
        screen.blit(full_heart, (x + 60, y))
    if health == 2:
        screen.blit(full_heart, (x, y))
        screen.blit(full_heart, (x + 30, y))
        screen.blit(empty_heart, (x + 60, y))
    if health == 1:
        screen.blit(full_heart, (x, y))
        screen.blit(empty_heart, (x + 30, y))
        screen.blit(empty_heart, (x + 60, y))
    if health == 0:
        screen.blit(empty_heart, (x, y))
        screen.blit(empty_heart, (x + 30, y))
        screen.blit(empty_heart, (x + 60, y))

# Loading assets
bg_image = pygame.image.load("assets/sky_bg.jpg").convert_alpha()
empty_heart = pygame.image.load("assets/empty_heart.png")
empty_heart = pygame.transform.scale(empty_heart, (25, 25))
full_heart = pygame.image.load("assets/full_heart.png")
full_heart = pygame.transform.scale(full_heart, (25, 25))

# Creating instances of planes
plane_1 = Plane(200, 310)
plane_2 = Plane(700, 310)

# Game loop
run = True
while run:

    clock.tick(FPS)

    # Draw background
    screen.blit(bg_image, (0, 0))

    # Display health bars
    draw_health_bar(plane_1.health, screen, 20, 20)
    draw_health_bar(plane_2.health, screen, 895, 20)

    plane_1.move(screen_width, screen_height, screen, plane_2)
    # plane_2.move(screen_width, screen_height, screen, plane_1)

    # Draw planes
    plane_1.draw(screen)
    plane_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()