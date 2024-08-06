import pygame
from plane import Plane
from plane import Bullet

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
    """
        Draws player health bar

        Args:
            health: player health
            screen: the game screen
            x: x coordinate the health bar will be drawn to
            y: y coordinate the health bar will be drawn to
        """
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
    if health <= 0:
        screen.blit(empty_heart, (x, y))
        screen.blit(empty_heart, (x + 30, y))
        screen.blit(empty_heart, (x + 60, y))

# Loading assets
bg_image = pygame.image.load("assets/sky_bg.jpg").convert_alpha()
empty_heart = pygame.image.load("assets/empty_heart.png")
empty_heart = pygame.transform.scale(empty_heart, (25, 25))
full_heart = pygame.image.load("assets/full_heart.png")
full_heart = pygame.transform.scale(full_heart, (25, 25))

# Creating bullet group
bullet_group = pygame.sprite.Group()

# Creating instances of planes
plane_1 = Plane(1, 200, 310, bullet_group)
plane_2 = Plane(2, 700, 310, bullet_group)
planes = [plane_1, plane_2]

# Game loop
run = True
while run:

    clock.tick(FPS)

    # Draw background
    screen.blit(bg_image, (0, 0))

    # Display health bars
    draw_health_bar(plane_1.health, screen, 20, 20)
    draw_health_bar(plane_2.health, screen, 895, 20)

    if plane_1.health > 0 and plane_2.health > 0:
        plane_1.move(screen_width, screen_height, plane_2)
        plane_2.move(screen_width, screen_height, plane_1)

    # Draw planes
    plane_1.draw(screen)
    plane_2.draw(screen)

    # End game if a player reaches 0 health
    if plane_1.health <= 0 or plane_2.health <= 0:
        if plane_1.health > plane_2.health:
            screen.blit(pygame.font.Font('assets/Grand9k Pixel.ttf', 40).render("Player 1 Wins!", True, (0, 0, 0)), (375, 100))
        if plane_1.health < plane_2.health:
            screen.blit(pygame.font.Font('assets/Grand9k Pixel.ttf', 40).render("Player 2 Wins!", True, (0, 0, 0)), (375, 100))
        if plane_1.health == plane_2.health:
            screen.blit(pygame.font.Font('assets/Grand9k Pixel.ttf', 40).render("Tie!", True, (0, 0, 0)), (475, 100))

    # Update and draw bullet group
    bullet_group.update(planes)
    bullet_group.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()