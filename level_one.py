import pygame
import config

from level import Level
from enemy import Enemy
from player import Player


class LevelOne(Level):
    def __init__(self, screen):
        super().__init__(screen, Player(100, 100))
       #  for i in range(5):
        self.enemies.add(Enemy(100, config.GROUND_Y - 100, "red"))
        self.enemies.add(Enemy(150, config.GROUND_Y - 100, "blue"))
        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)

    def draw(self):
        self.screen.fill(config.CLAY)

        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, config.HEIGHT - 70)

        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)
        for enemy in self.enemies:
            enemy_rect_cam = self.camera.apply(enemy.rect)
            self.screen.blit(enemy.img, enemy_rect_cam)

    
    def check_level_done(self):
        if len(self.enemies) == 0:
            return True
        else:
            return False


    def update(self):
        self.player.update(config.GRAVITY, config.GROUND_Y)
        self.camera.follow(self.player.get_rect(), config.WIDTH)
        self.enemies.update()
            
