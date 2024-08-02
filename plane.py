import pygame

class Plane():
    def __init__(self, x, y):
        self.flip = False
        self.rect = pygame.Rect((x, y, 80, 50))
        self.attacking = False
        self.health = 3

    def move(self, screen_width, screen_height, surface, target):
        speed = 10
        dx = 0
        dy = 0

        # Get keypresses
        key = pygame.key.get_pressed()

        # Movement
        if key[pygame.K_a]:
            dx = -speed
        if key[pygame.K_d]:
            dx = speed
        if key[pygame.K_w]:
            dy = -speed
        if key[pygame.K_s]:
            dy = speed
        # Attack
        if key[pygame.K_LSHIFT]:
            self.attack(surface, target)

        # Making sure players face each other
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

        # Making sure players stay on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height:
            dy = screen_height - self.rect.bottom
        if self.rect.top + dy < 0:
            dy = -self.rect.top

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 1

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)