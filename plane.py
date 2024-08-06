import pygame
# from bullet import Bullet

class Plane():
    """
    A class for the planes that the players play as an control

    Attributes:
        player: player number (either 1 or 2)
        flip: used to keep track of which direction a plane should face so that it faces 
              its opponent
        rect: rect object
        health: player health, player loses if this reaches 0
        bullet_group: used so that bullets can be added to the bullet group when player 
                      attacks
        last_shot: keeps track of when the player last attacked
        cooldown: the cooldown for player's attacks
    """
    def __init__(self, player, x, y, bullet_group):
        self.player = player
        self.flip = False
        self.rect = pygame.Rect((x, y, 80, 50))
        self.health = 3
        self.bullet_group = bullet_group
        self.bullet_vel = 10
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = 500

    def move(self, screen_width, screen_height, target):
        """
        Updates player based off user input (moving and attacking), makes sure that 
        players stay on screen, and make sure players face each other

        Args:
            planes: a list of planes that will be used to check for collisions
        """
        speed = 5
        dx = 0
        dy = 0

        # Get keypresses
        key = pygame.key.get_pressed()
        if self.player == 1:
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
            curr_time = pygame.time.get_ticks()
            if key[pygame.K_LSHIFT] and curr_time - self.last_shot > self.cooldown:
                self.attack()
                self.last_shot = curr_time
        
        if self.player == 2:
            # Movement
            if key[pygame.K_LEFT]:
                dx = -speed
            if key[pygame.K_RIGHT]:
                dx = speed
            if key[pygame.K_UP]:
                dy = -speed
            if key[pygame.K_DOWN]:
                dy = speed
            # Attack
            curr_time = pygame.time.get_ticks()
            if key[pygame.K_RSHIFT] and curr_time - self.last_shot > self.cooldown:
                self.attack()
                self.last_shot = curr_time

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
    
    def attack(self):
        """
        Adds a bullet to the bullet group and shoots in the appropriate direction based 
        off self.flip
        """
        if not self.flip:
            bullet = Bullet(self.rect.right, self.rect.centery, -1 * self.bullet_vel)
        else:
            bullet = Bullet(self.rect.left, self.rect.centery, self.bullet_vel)
        self.bullet_group.add(bullet)

    def draw(self, surface):
        """
        Draws player onto the screen

        Args:
            surface: the game screen
        """
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


class Bullet(pygame.sprite.Sprite):
    """
    A class for the bullets that players shoot out of their planes

    Attributes:
        image: how bullets appear in the game screen
        rect: rect object
        vel: bullet velocity
    """
    def __init__(self, x, y, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = vel
    
    def update(self, planes):
        """
        Updates bullet position and kills self if out of bounds or collides with a plane

        Args:
            planes: a list of planes that will be used to check for collisions
        """
        self.rect.x -= self.vel
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > 1000:
            self.kill()
        for plane in planes:
            if self.rect.colliderect(plane.rect):
                self.kill()
                plane.health -= 1
                if plane.health <= 0:
                    print(f"Player {plane.player}'s plane has been destroyed!")
                break