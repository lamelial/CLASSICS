import pygame
import config
import random

from level import Level
from enemy import Enemy
from player import Player
from gate import Gate


class LevelTwo(Level):
    def __init__(self, screen):
        super().__init__(screen, Player(100, config.GROUND_Y))
       #  for i in range(5):
        y_ground = config.GROUND_Y - 250
        start_x = config.WIDTH + 1000

        for i in range(10):
            x = start_x + i * random.randint(200, 500)  # stagger them
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)

        self.gate = Gate(x=1600, ground_y=config.GROUND_Y)
        self.objects.add(self.gate)

    def draw(self):
        self.screen.fill(config.CLAY)

        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, config.HEIGHT - 70)
        # pygame.draw.rect(self.screen, config.BLACK, (100, 100, 120, 80))     # house block
        #pygame.draw.polygon(self.screen, config.BLACK, [(100, 100), (100+120, 100), (100+60, 100-50)]) # roof

        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)
        for enemy in self.enemies:
            enemy_rect_cam = self.camera.apply(enemy.rect)
            self.screen.blit(enemy.img, enemy_rect_cam)
        
        for gate in self.objects:
            gate_rect_cam = self.camera.apply(gate.rect)
            self.screen.blit(gate.image, gate_rect_cam)

    
    def check_level_done(self):
        if len(self.enemies) == 0:
            return True
        else:
            return False


    def update(self):
        self.player.update()
        self.camera.follow(self.player.get_rect(), config.WIDTH)
        self.enemies.update()
        
    def handle_events(self, keys):
        super().handle_events(keys)
        player_rect = self.player.get_rect()

        for ob in self.objects:
            if ob.solid and player_rect.colliderect(ob.rect):
                if self.dx > 0:
                    player_rect.right = ob.rect.left
                elif self.dx < 0:
                    player_rect.left = ob.rect.right

                self.player.rect = player_rect

        for enemy in self.enemies:
            enemy.update()

            for ob in self.objects:
                if ob.solid and enemy.rect.colliderect(ob.rect):
                    if enemy.direction > 0: 
                        enemy.rect.right = ob.rect.left
                    else:
                        enemy.rect.left = ob.rect.right
                    enemy.direction *= -1

