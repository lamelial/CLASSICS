import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    SPEED = 5
    IMG_PATH = "assets/achilles.png"
    RANGE = 500

    def __init__(self, x, y, color):
        super().__init__()
        #self.forward_img = pygame.transform.scale(pygame.image.load(self.IMG_PATH).convert_alpha(), (int(80 * 1.5), int(120 * 1.5)))
        self.img = pygame.Surface((30, 30))  # Create a surface for the enemy
        self.img.fill(color)
        # self.img = self.forward_img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = True
        self.health = 5
        self.speed = 2
        self.start_x = x

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > self.start_x + 500 or self.rect.x < self.start_x - 500:
            self.speed *= -1

    def get_rect(self):
        return self.rect

    def get_img(self):
        return self.img

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
