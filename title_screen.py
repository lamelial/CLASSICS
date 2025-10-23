import pygame
import config


class TitleScreen:
    def __init__(self, screen):
        self.alpha = 0
        self.fade_speed = 3
        self.increasing = True
        self.screen = screen

    def draw(self):
        title_font = pygame.font.Font(None, 60)
        prompt_font = pygame.font.Font(None, 20)

        if self.increasing:
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.increasing = False
        else:
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                self.alpha = 0
                self.increasing = True

        self.screen.fill(config.BLACK)

        title_text = title_font.render("blah blahb lah", True, config.CLAY)
        title_rect = title_text.get_rect(
            center=(config.WIDTH // 2, config.HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        prompt_text = prompt_font.render("Press any key to begin", True, config.WHITE)
        prompt_surface = prompt_text.convert_alpha()
        prompt_surface.set_alpha(self.alpha)
        prompt_rect = prompt_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + 120))
        self.screen.blit(prompt_surface, prompt_rect)
