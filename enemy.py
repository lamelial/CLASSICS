import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    SPEED = 2
    IMG_PATH = "assets/warrior.png"

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(self.IMG_PATH).convert_alpha()
        self.backward_img = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.4), int(self.image.get_height() * 0.4)))
        self.forward_img = pygame.transform.flip(self.backward_img, True, False)
        #self.img = pygame.Surface((30, 30))  # Create a surface for the enemy
        #self.img.fill(color)
        self.img = self.forward_img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = True
        self.health = 5

        self.damage_timer = 0
        self.start_x = x

        self.speed = random.choice([1, 2, 3])         
        self.direction = random.choice([-1, 1])      
        self.patrol_range = random.randint(200, 500)  

    def update(self):
        # move according to direction and own speed
        self.rect.x += self.direction * self.speed

        # flip direction when hitting patrol bounds
        if self.rect.x > self.start_x + self.patrol_range:
            self.direction = -1
        elif self.rect.x < self.start_x - self.patrol_range:
            self.direction = 1

        # choose sprite based on direction
        if self.direction > 0:
            self.img = self.forward_img
        else:
            self.img = self.backward_img

        if self.damage_timer > 0:
            self.damage_timer -= 1
            self.img.set_alpha(180)
        else:
            self.img.set_alpha(255)

    def get_rect(self):
        return self.rect

    def get_img(self):
        return self.img

    def take_damage(self, player):
        self.health -= 1
        self.damage_timer = 10
        if self.health <= 0:
            self.kill()
            player.add_glory(10)
