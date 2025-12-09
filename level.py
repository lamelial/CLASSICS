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
        self.font = pygame.font.Font("assets/Romanica.ttf", 30)

    def update(self):
        self.enemies.update()
        self.objects.update()

    def draw(self):
        pass 

    def handle_events(self, keys, mouse_buttons):
        self.dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = 1
        if keys[pygame.K_SPACE]:
            self.player.jump()
        self.player.move(self.dx)

        # Attack with left mouse button or Q key
        if mouse_buttons[0] or keys[pygame.K_q]:
            self.player.attack(self.enemies, self.objects)

    def draw_key_pattern(self, surface, image, offset, y):
        img_width = image.get_width()
        start_x = int(offset) % img_width
        for x in range(-img_width, config.WIDTH + img_width, img_width):
            surface.blit(image, (x - start_x, y))
