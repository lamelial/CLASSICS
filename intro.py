import pygame
import config
import random

from boat import Boat
from camera import Camera
from level import Level

class Intro(Level):
    def __init__(self, screen):
        super().__init__(screen, Boat(100, config.HEIGHT - 275))
        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)
        self.wave_img = pygame.image.load("assets/waves.png").convert_alpha()
        self.wave_img = pygame.transform.scale_by(self.wave_img, 0.25)
        self.screen = screen
        self.camera = Camera(screen.get_size()[0], screen.get_size()[1])

        self.fleet = []
        self.fleet.append(self.player)

        spacing_min = 200
        spacing_max = 500

        y = config.HEIGHT - 275
        x = 100  # starting x-position

        for i in range(15):
            self.fleet.append(Boat(x, y))
            x -= random.randint(spacing_min, spacing_max)



    def draw(self):
        self.screen.fill(config.CLAY)

        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        self.draw_key_pattern(self.screen, self.wave_img, self.camera.offset_x * 0.5, config.HEIGHT - 50)

        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)

        for boat in self.fleet:
            rect_cam = self.camera.apply(boat.get_rect())
            self.screen.blit(boat.get_img(), rect_cam)


    def update(self):
        #self.camera.follow(self.player.get_rect(), config.WIDTH)
        keys = pygame.key.get_pressed()
        

    def handle_events(self, keys):
        dx = 0

        if keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_LEFT]:
            dx = -1

        # move all boats together
        if dx != 0:
            for boat in self.fleet:
                boat.move(dx)   # assumes Boat has move(dx) similar to Player.move

    def check_level_done(self):
        yah = True
        for boat in self.fleet:
            if boat.rect.left < config.WIDTH:
                yah = False
        return yah
            
