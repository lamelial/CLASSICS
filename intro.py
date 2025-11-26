# intro.py
import pygame
import config
import random

from boat import Boat
from camera import Camera
from level import Level
from textfx import TextSequence, TextLine   # ✅ new import


class Intro(Level):
    def __init__(self, screen):
        super().__init__(screen, Boat(100, config.HEIGHT - 275))

        self.screen = screen
        self.camera = Camera(screen.get_size()[0], screen.get_size()[1])

        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)

        self.wave_img = pygame.image.load("assets/waves.png").convert_alpha()
        self.wave_img = pygame.transform.scale_by(self.wave_img, 0.25)

        self.font = pygame.font.Font("assets/Romanica.ttf", 40)

        # initial prompt
        self.text_alpha = 255
        self.started = False

        self.text_seq = TextSequence()
        self.text_seq.add_line(TextLine("PROPAGANDA ONE.",
                                        self.font, 180))
        self.text_seq.add_line(TextLine("PROPAGANDA TWO.",
                                        self.font, 180))
        self.text_seq.add_line(TextLine("OBJECTIVE: RESCUE HELEN",
                                        self.font, 180))

        # fleet setup ...
        self.fleet = [self.player]
        spacing_min = 200
        spacing_max = 500
        y = config.HEIGHT - 275
        x = 100
        for _ in range(5):
            x -= random.randint(spacing_min, spacing_max)
            self.fleet.append(Boat(x, y))

    def update(self):
        # fade out the initial prompt once started
        if self.started and self.text_alpha > 0:
            self.text_alpha -= 5
            if self.text_alpha < 0:
                self.text_alpha = 0

        if self.started and self.text_alpha == 0 and not self.text_seq.active and not self.text_seq.finished:
            self.text_seq.start()

        # update text sequence
        self.text_seq.update()

    def handle_events(self, keys):
        dx = 0

        if keys[pygame.K_RIGHT]:
            dx = 1
            if not self.started:
                self.started = True
        elif keys[pygame.K_LEFT]:
            dx = -1

        if dx != 0:
            for boat in self.fleet:
                boat.move(dx)

    def draw(self):
        self.screen.fill(config.CLAY)

        # borders/waves...
        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        self.draw_key_pattern(self.screen, self.wave_img, self.camera.offset_x * 0.5, config.HEIGHT - 70)
        self.draw_key_pattern(self.screen, self.wave_img, self.camera.offset_x * 0.5, config.HEIGHT - 30)
        self.draw_key_pattern(self.screen, self.wave_img, self.camera.offset_x * 0.5, config.HEIGHT - 120)

        # fleet
        for boat in self.fleet:
            rect_cam = self.camera.apply(boat.get_rect())
            self.screen.blit(boat.get_img(), rect_cam)

        # initial prompt
        if self.text_alpha > 0:
            self.draw_centered_text("PRESS RIGHT TO SAIL FOR TROY",
                                    self.font, 120, self.text_alpha)

        # narrative sequence
        self.text_seq.draw(self.screen)

    def check_level_done(self):
        # all boats gone AND sequence finished
        all_past = all(boat.rect.left >= config.WIDTH for boat in self.fleet)
        return all_past and self.text_seq.is_finished()

    def draw_centered_text(self, text, font, y, alpha=255):
        surf = font.render(text, True, (0, 0, 0))
        surf.set_alpha(alpha)
        rect = surf.get_rect(center=(config.WIDTH // 2, y))
        self.screen.blit(surf, rect)

    def draw_key_pattern(self, surface, image, offset, y):
        img_width = image.get_width()
        start_x = int(offset) % img_width
        for x in range(-img_width, config.WIDTH + img_width, img_width):
            surface.blit(image, (x - start_x, y))
