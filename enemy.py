import pygame
import random


class Enemy(pygame.sprite.Sprite):
    _SPEED = 5
    _IMG_PATH = "assets/achilles.png"

    def __init__(self, x, y):
        super().__init__()
        self.forward_img = pygame.transform.scale(pygame.image.load(self._IMG_PATH).convert_alpha(), (int(80 * 1.5), int(120 * 1.5)))
        self.img = self.forward_img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = True

    def move(self, dx):
        self.rect.x += dx * self._SPEED

    def update(self):
        print(self.rect.x)
        if random.randint(1, 10) == 8:
            self.move(-1)

    def get_rect(self):
        return self.rect

    def get_img(self):
        return self.img
