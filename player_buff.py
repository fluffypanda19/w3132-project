import pygame
import plane, buff_reference

class Buff(pygame.sprite.Sprite):
    """
    A class for the bullets that players shoot out of their planes

    Attributes:
        buff_type: buff-type determines what type of effect player gets
                   when collecting it
        duration: duration of how long the buff lasts
        image: how buffs appear in the game screen
        rect: rect object
        vel: buff velocity
    """
    def __init__(self, x, y, buff_type):
        pygame.sprite.Sprite.__init__(self)
        self.buff_type = buff_type
        self.duration = buff_reference.buff_durations[buff_type]
        self.image = pygame.Surface((20, 20))
        self.image.fill(buff_reference.buff_images[buff_type])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 4
    
    def update(self, planes):
        """
        Updates bullet position and kills self if out of bounds or collides with a plane

        Args:
            planes: a list of planes that will be used to check for collisions
        """
        # Kills self if out of bounds
        self.rect.y += self.vel
        if self.rect.top > 500:
            self.kill()

        # Collision detection
        for plane in planes:
            if self.rect.colliderect(plane.rect):
                self.kill()
                if self.buff_type == "heal" and plane.health < 3:
                    plane.health += 1
                else:
                    plane.buff_dict.update({self.buff_type : pygame.time.get_ticks()})
                break