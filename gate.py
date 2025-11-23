import pygame
import config

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, ground_y):
        super().__init__()

        # size of the gate
        width = 220
        height = 300

        # intact image
        self.intact_img = pygame.Surface((width, height), pygame.SRCALPHA)
        self._draw_intact(self.intact_img)

        # broken image
        self.broken_img = pygame.Surface((width, height), pygame.SRCALPHA)
        self._draw_broken(self.broken_img)

        self.image = self.intact_img
        self.rect = self.image.get_rect(midbottom=(x, ground_y))

        self.health = 3
        self.solid = True

    def _draw_intact(self, surf):
        w, h = surf.get_size()

        pygame.draw.rect(surf, config.BLACK, (0, h//3, w, h - h//3))

        tooth_width = 24
        tooth_height = h//4
        x = 0
        while x < w:
            pygame.draw.rect(surf, config.BLACK, (x, 0, tooth_width, tooth_height))
            x += tooth_width + 8

    def _draw_broken(self, surf):
        w, h = surf.get_size()

        pygame.draw.polygon(
            surf,
            config.BLACK,
            [
                (0, h), (0, h//2),
                (w//4, h//2 + 15),
                (w//2, h//2 - 10),
                (3*w//4, h//2 + 20),
                (w, h//2),
                (w, h)
            ]
        )

        # a few chunks
        pygame.draw.rect(surf, config.BLACK, (w//4 - 10, h - 20, 20, 20))
        pygame.draw.rect(surf, config.BLACK, (w//2 - 8, h - 18, 16, 18))
        pygame.draw.rect(surf, config.BLACK, (3*w//4 - 12, h - 22, 24, 22))

    def take_damage(self):
        if not self.solid:
            return

        self.health -= 1
        if self.health <= 0:
            self.break_gate()

    def break_gate(self):
        self.solid = False
        bottom = self.rect.bottom
        self.image = self.broken_img
        self.rect = self.image.get_rect(midbottom=(self.rect.centerx, bottom))
