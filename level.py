import pygame
from player import Player
from camera import Camera
import config


class Level:
    def __init__(self, screen, player):
        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.background = None
        self.player = player
        self.screen = screen
        self.camera = Camera(screen.get_size()[0], screen.get_size()[1])

    def update(self):
        self.enemies.update()
        self.objects.update()

    def draw(self):
        pass

    def handle_events(self, keys):
        self.dx = 0
        if keys[pygame.K_LEFT]:
            self.dx = -1
        if keys[pygame.K_RIGHT]:
            self.dx = 1
        if keys[pygame.K_SPACE]:
            self.player.jump()
        self.player.move(self.dx)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.player.attack(self.enemies, self.objects)

    def draw_key_pattern(self, surface, image, offset, y):
        img_width = image.get_width()
        start_x = int(offset) % img_width
        for x in range(-img_width, config.WIDTH + img_width, img_width):
            surface.blit(image, (x - start_x, y))
