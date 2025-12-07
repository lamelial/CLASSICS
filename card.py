import pygame
import config


class Card:
    def __init__(self, screen):
        self.alpha = 0
        self.fade_speed = 3
        self.increasing = True
        self.screen = screen
        self.font = pygame.font.Font("assets/Romanica.ttf", 60)


    def draw_title(self):
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

        title_text = self.font.render("FOR HELEN", True, config.CLAY)
        title_rect = title_text.get_rect(
            center=(config.WIDTH // 2, config.HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        prompt_text = prompt_font.render("Press any key to begin", True, config.WHITE)
        prompt_surface = prompt_text.convert_alpha()
        prompt_surface.set_alpha(self.alpha)
        prompt_rect = prompt_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + 120))
        self.screen.blit(prompt_surface, prompt_rect)

    def draw_agam(self):
        self.screen.fill(config.BLACK)

        banner_color = config.CLAY
        banner_height = 80
        banner_x = 100
        banner_y = config.HEIGHT // 4 - banner_height // 2
        banner_width = config.WIDTH - 200
        banner_rect = pygame.Rect(banner_x, banner_y, banner_width, banner_height)
        pygame.draw.rect(self.screen, banner_color, banner_rect)

        title_text = self.font.render("put text in this banner", True, config.BLACK)
        title_rect = title_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        agam = pygame.image.load("assets/agam.png").convert_alpha()
        agam = pygame.transform.scale_by(agam, 0.4)
        agam_rect = agam.get_rect()
        agam_rect.center = (config.WIDTH // 2 - 30, config.HEIGHT // 2 + 20)
        self.screen.blit(agam, agam_rect)

