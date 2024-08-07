import pygame
import player_buff
import buff_reference

class Plane():
    """
    A class for the planes that the players play as an control

    Attributes:
        player: player number (either 1 or 2)
        flip: used to keep track of which direction a plane should face so that it faces 
              its opponent
        rect: rect object
        health: player health, player loses if this reaches 0
        shielded: negates next instance of damage taken if true
        speed: speed at which player moves
        bullet_group: the bullet group that a bullet instance (created by player attacks)
                      will be added to
        last_shot: keeps track of when the player last attacked
        cooldown: the cooldown for player's attacks
        buff_dict: dictionary of buffs in the form of (buff_type : time_applied)
    """
    def __init__(self, player, x, y, bullet_group):
        self.player = player
        self.flip = False
        self.rect = pygame.Rect((x, y, 60, 40))
        self.health = 3
        self.shielded = False
        self.speed = 5
        self.bullet_group = bullet_group
        self.bullet_vel = 10
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = 500
        self.buff_dict = {}

    def move(self, screen_width, screen_height, target):
        """
        Updates player based off user input (moving and attacking), makes sure that 
        players stay on screen, and make sure players face each other

        Args:
            planes: a list of planes that will be used to check for collisions
        """
        dx = 0
        dy = 0

        # Get keypresses
        key = pygame.key.get_pressed()
        if self.player == 1:
            # Movement
            if key[pygame.K_a]:
                dx = -self.speed
            if key[pygame.K_d]:
                dx = self.speed
            if key[pygame.K_w]:
                dy = -self.speed
            if key[pygame.K_s]:
                dy = self.speed
            # Attack
            curr_time = pygame.time.get_ticks()
            if key[pygame.K_LSHIFT] and curr_time - self.last_shot > self.cooldown:
                self.attack()
                self.last_shot = curr_time
        
        if self.player == 2:
            # Movement
            if key[pygame.K_LEFT]:
                dx = -self.speed
            if key[pygame.K_RIGHT]:
                dx = self.speed
            if key[pygame.K_UP]:
                dy = -self.speed
            if key[pygame.K_DOWN]:
                dy = self.speed
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
        
        # Storing expired buffs for removal
        buffs_to_remove = []
        for buff in self.buff_dict:
            if buff in buff_reference.buff_durations:
                if pygame.time.get_ticks() - self.buff_dict[buff] > buff_reference.buff_durations[buff]:
                    buffs_to_remove.append(buff)
            if buff in buff_reference.debuff_durations:
                if pygame.time.get_ticks() - self.buff_dict[buff] > buff_reference.debuff_durations[buff]:
                    buffs_to_remove.append(buff)

        # Removing expired buffs
        for buff in buffs_to_remove:
            del self.buff_dict[buff]

        # Adjusting player speed based off "slowed" and "speed" buffs
        if "slowed" in self.buff_dict and "speed" in self.buff_dict:
            self.speed = 5
        elif "slowed" in self.buff_dict:
            self.speed = 2
        elif "speed" in self.buff_dict:
            self.speed = 8
        else:
            self.speed = 5
        
        # Adjusting bullet velocity based off "speedy_bullets" buff
        if "speedy_bullets" in self.buff_dict:
            self.bullet_vel = 20
        else:
            self.bullet_vel = 10

        # Adjusting player fire rate based off "rapid_fire" buff
        if "rapid_fire" in self.buff_dict:
            self.cooldown = 200
        else:
            self.cooldown = 500
        
        # Applying "shield" if in buff_dict
        if "shield" in self.buff_dict:
            self.shielded = True
        else:
            self.shielded = False
            
    def attack(self):
        """
        Adds a bullet to the bullet group and shoots in the appropriate direction based 
        off self.flip
        """
        if not self.flip:
            bullet = Bullet(self.rect.right, self.rect.centery, -1 * self.bullet_vel, 
                            "freezing_bullets" in self.buff_dict)
        else:
            bullet = Bullet(self.rect.left, self.rect.centery, self.bullet_vel,
                            "freezing_bullets" in self.buff_dict)
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
        player: player that is shooting this bullet
        freezing: slows player movement on-hit if true (obtained from freezing bullets 
                  buff)
    """
    def __init__(self, x, y, vel, freezing = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        if freezing:
            self.image.fill(buff_reference.buff_images.get("freezing_bullets")) 
        else:
            self.image.fill((0, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = vel
        self.freezing = freezing
    
    def update(self, planes):
        """
        Updates bullet position and kills self if out of bounds or collides with a plane

        Args:
            planes: a list of planes that will be used to check for collisions
        """
        # Kills self if out of bounds
        self.rect.x -= self.vel
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > 1000:
            self.kill()

        # Collision detection
        for plane in planes:
            if self.rect.colliderect(plane.rect):
                self.kill()

                # Applies slowed debuff if bullet is freezing
                if self.freezing:
                    plane.buff_dict.update({"slowed" : pygame.time.get_ticks()})

                # Removes "shield" buff if shielded, else decrement plane.health
                if plane.shielded:
                    del plane.buff_dict["shield"]
                else:
                    plane.health -= 1

                # Print message if player reaches 0 health
                if plane.health <= 0:
                    print(f"Player {plane.player}'s plane has been destroyed!")
                break


class Sky_Bullet(pygame.sprite.Sprite):
    """
    A class for the bullets that fall from the sky

    Attributes:
        image: how bullets appear in the game screen
        rect: rect object
        vel: bullet velocity
        bullet_group: the bullet group this instance will be added to
    """
    def __init__(self, x, y, bullet_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 4
        self.bullet_group = bullet_group
    
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
                
                # Removes "shield" buff if shielded, else decrement plane.health
                if plane.shielded:
                    del plane.buff_dict["shield"]
                else:
                    plane.health -= 1

                # Print message if player reaches 0 health
                if plane.health <= 0:
                    print(f"Player {plane.player}'s plane has been destroyed!")
                break