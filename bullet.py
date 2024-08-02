import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = vel
    
    def update(self):
        self.rect.x -= self.vel
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > 1000:
            self.kill()