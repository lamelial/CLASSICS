import pygame
import config
import random
import enum

from level import Level
from enemy import Enemy
from player import Player
from gate import Gate
from textfx import TextLine, TextSequence

class State(enum.Enum):
    START = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    RETURN = 5

class LevelOne(Level):
    def __init__(self, screen):
        super().__init__(screen, Player(100, config.GROUND_Y))
        # for i in range(5):
        y_ground = config.GROUND_Y - 250
        start_x = config.WIDTH + 1000
        self.timer = 1000
        for i in range(5):
            x = start_x + i * random.randint(200, 500)  # stagger them
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)
        self.showing_card = True
        self.dialogue_triggered = False
        self.dialogue = TextSequence(config.BLACK)
        self.dialogue.add_line(TextLine("THE WALLS OF TROY", self.font, 100, hold_frames=50))
        self.state = State.START
        self.gate_x = 1200

        # card
        self.showing_card = True

        self.card_sequence = TextSequence(config.CLAY)
        self.card_sequence.add_line(TextLine("LEVEL ONE", self.font, 100))
        self.card_sequence.add_line(TextLine("WE HAVE ARRIVED AT TROY", self.font, 100))
        self.card_sequence.add_line(TextLine("FIND AND RESCUE HELEN", self.font, 100))

        self.card_sequence.start()

    def draw(self):
        if self.state == State.GAME_OVER:
            return

        self.screen.fill(config.CLAY)
        if self.showing_card:
            self.draw_card()
            return
        
        if self.dialogue_triggered:
            self.dialogue.draw(self.screen)

        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        self.draw_key_pattern(self.screen, self.meander_img, self.camera.offset_x * 0.5, config.HEIGHT - 70)
        self.draw_gate(self.screen, self.gate_x, config.GROUND_Y) # drawing player in here sorry

        for enemy in self.enemies:
            enemy_rect_cam = self.camera.apply(enemy.rect)
            self.screen.blit(enemy.img, enemy_rect_cam)
        
        # for gate in self.objects:
        #     gate_rect_cam = self.camera.apply(gate.rect)
        #     self.screen.blit(gate.image, gate_rect_cam)
        font = pygame.font.Font("assets/Romanica.ttf", 12)
        glory_surf = font.render("GLORY: " + str(self.player.glory), True, config.BLACK)
        glory_rect = glory_surf.get_rect(topleft=(10, 4))
        self.screen.blit(glory_surf, glory_rect)


    def check_level_done(self):
        if self.state == State.RETURN:
            return True
        else:
            return False



    def update(self):
        if self.state == State.GAME_OVER:
            self.level_over()
            return
        
        if self.showing_card:
            self.card_sequence.update()
            if self.card_sequence.is_finished():
                self.showing_card = False
                self.state = State.PLAYING
            return
         
        self.player.update()
        self.camera.follow(self.player.get_rect(), config.WIDTH)
        self.enemies.update()

        if len(self.enemies) == 0:
            self.state = State.GAME_OVER

        if self.dialogue_triggered:
            self.dialogue.update()
            if self.dialogue.is_finished():
                self.dialogue_triggered = False
        
    def handle_events(self, keys):

        if self.state == State.GAME_OVER:
            if keys[pygame.K_SPACE]:
                self.state = State.RETURN
                return
            
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

    def draw_gate(self, surface, x_world, ground_y, label="ΜYΣΙΑ"):
        GATE_COLOR = config.BLACK
        PILLAR_WIDTH = 40
        GATE_HEIGHT = 250
        GATE_WIDTH = 200
        BEAM_HEIGHT = 25

        # WORLD-SPACE rects
        left_pillar_world = pygame.Rect(x_world, ground_y - GATE_HEIGHT, PILLAR_WIDTH, GATE_HEIGHT)
        right_pillar_world = pygame.Rect(x_world + GATE_WIDTH, ground_y - GATE_HEIGHT, PILLAR_WIDTH, GATE_HEIGHT)
        beam_world = pygame.Rect(x_world, ground_y - GATE_HEIGHT - BEAM_HEIGHT,
                                GATE_WIDTH + PILLAR_WIDTH, BEAM_HEIGHT)

        # CAMERA-SPACE rects for drawing
        left_pillar = self.camera.apply(left_pillar_world)
        right_pillar = self.camera.apply(right_pillar_world)
        beam = self.camera.apply(beam_world)

        #wall_bg = pygame.Rect(x_world + GATE_WIDTH + PILLAR_WIDTH, ground_y - 100, 4000, 100)
        #wall = self.camera.apply(wall_bg)
        #pygame.draw.rect(surface, GATE_COLOR, wall)

        # draw pillars & beam
        pygame.draw.rect(surface, GATE_COLOR, left_pillar)

        # draw player (already doing this correctly)
        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)

        pygame.draw.rect(surface, GATE_COLOR, right_pillar)
        pygame.draw.rect(surface, GATE_COLOR, beam)


        # label in camera space
        greek_font = pygame.font.Font("assets/FreeSerif.ttf", 20)
        label_surf = greek_font.render(label, True, config.CLAY)
        label_rect = label_surf.get_rect(center=(beam.centerx, beam.top + 10))  # tweak as you like
        surface.blit(label_surf, label_rect)

        # COLLISION: still world space
        passage_rect_world = pygame.Rect(
            x_world + PILLAR_WIDTH,
            ground_y - GATE_HEIGHT - BEAM_HEIGHT,
            GATE_WIDTH,
            GATE_HEIGHT + BEAM_HEIGHT,
        )

        if not self.dialogue_triggered and self.player.get_rect().colliderect(passage_rect_world):
            print("collide")
            self.trigger_dialogue()
            self.dialogue_triggered = True



    def trigger_dialogue(self):
        self.dialogue.start()

    def level_over(self):
        self.timer -= 1

        self.screen.fill(config.BLACK)

        big_font = pygame.font.Font("assets/Romanica.ttf", 36)
        small_font = pygame.font.Font("assets/Romanica.ttf", 24)

        lines = [
            "TEST LEVEL COMPLETE",
            f"GLORY: {self.player.glory}",
        ]

        title_surf = big_font.render("DONE", True, config.CLAY)
        title_rect = title_surf.get_rect(center=(config.WIDTH // 2, 100))
        self.screen.blit(title_surf, title_rect)

        start_y = 180
        line_spacing = 40

        for i, text in enumerate(lines):
            surf = small_font.render(text, True, config.CLAY)
            rect = surf.get_rect(center=(config.WIDTH // 2, start_y + i * line_spacing))
            self.screen.blit(surf, rect)

        if self.timer < 700:
            hint_surf = small_font.render("PRESS SPACE TO CONTINUE", True, config.CLAY)
            hint_rect = hint_surf.get_rect(center=(config.WIDTH // 2, config.HEIGHT - 80))
            self.screen.blit(hint_surf, hint_rect)

        if self.timer <= 0:
            self.state = State.RETURN


