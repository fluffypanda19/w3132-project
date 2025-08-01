import pygame
import random
from plane import Plane
from plane import Bullet
from plane import Sky_Bullet
from player_buff import Buff
import buff_reference

pygame.init()

# Create game window
screen_width = 1000
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("1v1 Plane Game")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

def draw_health_bar(plane, screen, x, y):
    """
        Draws player health bar

        Args:
            plane: player
            screen: the game screen
            x: x coordinate the health bar will be drawn to
            y: y coordinate the health bar will be drawn to
        """
    if plane.health == 3:
        screen.blit(full_heart, (x, y))
        screen.blit(full_heart, (x + 30, y))
        screen.blit(full_heart, (x + 60, y))
    if plane.health == 2:
        screen.blit(full_heart, (x, y))
        screen.blit(full_heart, (x + 30, y))
        screen.blit(empty_heart, (x + 60, y))
    if plane.health == 1:
        screen.blit(full_heart, (x, y))
        screen.blit(empty_heart, (x + 30, y))
        screen.blit(empty_heart, (x + 60, y))
    if plane.health <= 0:
        screen.blit(empty_heart, (x, y))
        screen.blit(empty_heart, (x + 30, y))
        screen.blit(empty_heart, (x + 60, y))
    if plane.shielded:
        screen.blit(shield, (x + 90, y))

# Loading assets
bg_image = pygame.image.load("assets/sky_bg.jpg").convert_alpha()
empty_heart = pygame.image.load("assets/empty_heart.png")
empty_heart = pygame.transform.scale(empty_heart, (25, 25))
full_heart = pygame.image.load("assets/full_heart.png")
full_heart = pygame.transform.scale(full_heart, (25, 25))
shield = pygame.image.load("assets/shield.png")
shield = pygame.transform.scale(shield, (25, 25))

# Creating bullet group
bullet_group = pygame.sprite.Group()
sky_bullet_group = pygame.sprite.Group()

# Sky bullet cooldown and last shot variables
sky_last_shot = pygame.time.get_ticks()
sky_cooldown = 150

# Creating buff group
buff_group = pygame.sprite.Group()

# Buff drop cooldown and last spawned variables
buff_last_spawn = pygame.time.get_ticks()
buff_drop_cooldown = 10000

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
    draw_health_bar(plane_1, screen, 20, 20)
    draw_health_bar(plane_2, screen, 865, 20)

    # Allow player movement while both players' health are not 0
    # If a player reaches 0 health, movement is no longer allowed and we get the end game screen
    if plane_1.health > 0 and plane_2.health > 0:
        plane_1.move(screen_width, screen_height, plane_2)
        plane_2.move(screen_width, screen_height, plane_1)
        
        # Periodically shoots random bullets down from the sky
        curr_time = pygame.time.get_ticks()
        if curr_time - sky_last_shot > sky_cooldown:
                bullet = Sky_Bullet(random.randint(0, 1000), 0, sky_bullet_group)
                sky_bullet_group.add(bullet)
                sky_last_shot = curr_time

        # Periodically drops buffs from the sky
        if curr_time - buff_last_spawn > buff_drop_cooldown:
                buff = Buff(random.randint(0, 1000), 0, random.choice(list(buff_reference.buff_durations.keys())))
                buff_group.add(buff)
                buff_last_spawn = curr_time
        
        # Update bullet and buff groups
        bullet_group.update(planes)
        sky_bullet_group.update(planes)
        buff_group.update(planes)
    
    # Draw planes, bullet groups, and buff group
    plane_1.draw(screen)
    plane_2.draw(screen)
    bullet_group.draw(screen)
    sky_bullet_group.draw(screen)
    buff_group.draw(screen)

    # Print victory message
    if plane_1.health <= 0 or plane_2.health <= 0:
        if plane_1.health > plane_2.health:
            screen.blit(pygame.font.Font('assets/Grand9k Pixel.ttf', 40).render("Player 1 Wins!", True, (0, 0, 0)), (375, 100))
        if plane_1.health < plane_2.health:
            screen.blit(pygame.font.Font('assets/Grand9k Pixel.ttf', 40).render("Player 2 Wins!", True, (0, 0, 0)), (375, 100))
        if plane_1.health == plane_2.health:
            screen.blit(pygame.font.Font('assets/Grand9k Pixel.ttf', 40).render("Tie!", True, (0, 0, 0)), (475, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()