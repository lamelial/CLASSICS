import pygame
import config
from level import Level
from enemy import Enemy


def draw_key_pattern(surface, image, offset, y):
    img_width = image.get_width()
    start_x = int(offset) % img_width
    for x in range(-img_width, config.WIDTH + img_width, img_width):
        surface.blit(image, (x - start_x, y))


class LevelOne(Level):
    def __init__(self, screen):
        super().__init__(screen)
        self.enemy = Enemy(100, config.GROUND_Y - 100)
        self.enemies.add(self.enemy)
        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)

    def draw(self):
        self.screen.fill(config.CLAY)

        draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, config.HEIGHT - 70)

        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)
        enemy_rect_cam = self.camera.apply(self.enemy.get_rect())
        self.screen.blit(self.enemy.get_img(), enemy_rect_cam)

    def update(self):
        self.player.update(config.GRAVITY, config.GROUND_Y)
        self.camera.follow(self.player.get_rect(), config.WIDTH)
        self.enemies.update()
