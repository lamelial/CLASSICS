import pygame
from player import Player
from camera import Camera


class Level:
    def __init__(self, screen):
        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.background = None
        self.player = Player(100, 600)
        self.screen = screen
        self.camera = Camera(screen.get_size()[0], screen.get_size()[1])

    def update(self):
        self.enemies.update()
        self.objects.update()

    def draw(self):
        pass

    def handle_events(self, keys):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_SPACE]:
            self.player.jump()
        self.player.move(dx)
