import pygame
import config
import random

from level import Level
from enemy import Enemy
from player import Player
from gate import Gate
from textfx import TextLine, TextSequence


class LevelOne(Level):
    def __init__(self, screen):
        super().__init__(screen, Player(100, config.GROUND_Y))
        # for i in range(5):
        y_ground = config.GROUND_Y - 250
        start_x = config.WIDTH + 1000

        for i in range(5):
            x = start_x + i * random.randint(200, 500)  # stagger them
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)
        self.showing_card = True

        self.gate_x = 1200

        # card
        self.showing_card = True

        self.card_sequence = TextSequence(config.CLAY)
        self.card_sequence.add_line(TextLine("LEVEL ONE", self.font, 100))
        self.card_sequence.add_line(TextLine("WE HAVE ARRIVED AT TROY", self.font, 100))
        self.card_sequence.add_line(TextLine("FIND AND RESCUE HELEN", self.font, 100))

        self.card_sequence.start()

    def draw(self):
        self.screen.fill(config.CLAY)
        if self.showing_card:
            self.draw_card()
            return

        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, config.HEIGHT - 70)
        self.draw_gate(self.screen, self.gate_x - self.camera.offset_x, config.GROUND_Y) # drawing player in here sorry

        for enemy in self.enemies:
            enemy_rect_cam = self.camera.apply(enemy.rect)
            self.screen.blit(enemy.img, enemy_rect_cam)
        
        # for gate in self.objects:
        #     gate_rect_cam = self.camera.apply(gate.rect)
        #     self.screen.blit(gate.image, gate_rect_cam)


    def check_level_done(self):
        if len(self.enemies) == 0:
            return True
        else:
            return False


    def update(self):
        if self.showing_card:
            self.card_sequence.update()
            if self.card_sequence.is_finished():
                self.showing_card = False
            return
         
        self.player.update()
        self.camera.follow(self.player.get_rect(), config.WIDTH)
        self.enemies.update()
        
    def handle_events(self, keys):
        if self.showing_card:
            if keys[pygame.K_SPACE]:
                self.showing_card = False # SKIP
            else:
                return
            
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

    def draw_card(self):
        self.screen.fill(config.BLACK)
        self.card_sequence.draw(self.screen)

    def draw_gate(self, surface, x, ground_y, label="ΜYΣΙΑ"):
        GATE_COLOR = (0, 0, 0)  # vase-black
        PILLAR_WIDTH = 40
        GATE_HEIGHT = 250
        GATE_WIDTH = 300
        BEAM_HEIGHT = 25

        # pillars
        left_pillar = pygame.Rect(x, ground_y - GATE_HEIGHT, PILLAR_WIDTH, GATE_HEIGHT)
        right_pillar = pygame.Rect(x + GATE_WIDTH, ground_y - GATE_HEIGHT, PILLAR_WIDTH, GATE_HEIGHT)

        pygame.draw.rect(surface, GATE_COLOR, left_pillar)
        # so that the player walks through the gate. bad code seperation yeah whatever
        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)
        
        pygame.draw.rect(surface, GATE_COLOR, right_pillar)

        # beam
        beam = pygame.Rect(x, ground_y - GATE_HEIGHT - BEAM_HEIGHT, GATE_WIDTH + PILLAR_WIDTH, BEAM_HEIGHT)
        pygame.draw.rect(surface, GATE_COLOR, beam)

        # label text
        greek_font = pygame.font.Font("assets/FreeSerif.ttf", 32)
        label_surf = greek_font.render(label, True, config.CLAY)
        label_rect = label_surf.get_rect(center=(x + GATE_WIDTH/2 +10, ground_y - GATE_HEIGHT - BEAM_HEIGHT // 2))
        surface.blit(label_surf, label_rect)

        #return pygame.Rect(x, ground_y - GATE_HEIGHT, 200 + PILLAR_WIDTH, GATE_HEIGHT + BEAM_HEIGHT)
