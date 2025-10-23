import pygame
import config
from level import Level


def draw_key_pattern(surface, image, offset, y):
    img_width = image.get_width()
    start_x = int(offset) % img_width
    for x in range(-img_width, config.WIDTH + img_width, img_width):
        surface.blit(image, (x - start_x, y))


class LevelOne(Level):
    def __init__(self, screen):
        super().__init__(screen)

        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)

    def draw(self):
        self.screen.fill(config.CLAY)
        pygame.draw.rect(self.screen, config.BLACK, (0, config.GROUND_Y, config.WIDTH, 50))

        draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        self.player.draw(self.screen)
        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)

    def update(self):
        self.player.update(config.GRAVITY, config.GROUND_Y)