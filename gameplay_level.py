import pygame
import config
import enum
from level import Level
from player import Player
from textfx import TextLine, TextSequence


class State(enum.Enum):
    START = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    RETURN = 5


class GameplayLevel(Level):
    """Base class for combat/gameplay levels with players fighting enemies"""
    
    def __init__(self, screen, level_name, level_description):
        super().__init__(screen, Player(100, config.GROUND_Y))
        
        self.level_name = level_name
        self.level_description = level_description
        self.state = State.START
        self.showing_card = True
        self.dialogue_triggered = False
        self.timer = 1000
        
        # Decorative elements
        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)
        
        # Level card sequence
        self.card_sequence = TextSequence(config.CLAY)
        self.card_sequence.add_line(TextLine(level_name, self.font, 100))
        self.card_sequence.add_line(TextLine(level_description, self.font, 100))
        self.setup_card_sequence()
        self.card_sequence.start()
        
        # Dialogue system
        self.dialogue = TextSequence(config.BLACK)
        self.setup_dialogue()
        
    def setup_card_sequence(self):
        """Override this to add additional card text lines"""
        pass
    
    def setup_dialogue(self):
        """Override this to set up level-specific dialogue"""
        pass
    
    def setup_enemies(self):
        """Override this to spawn enemies for the level"""
        pass
    
    def setup_objects(self):
        """Override this to place gates, obstacles, etc."""
        pass
    
    def update(self):
        if self.state == State.GAME_OVER:
            self.level_over()
            return
        
        if self.showing_card:
            self.card_sequence.update()
            if self.card_sequence.is_finished():
                self.showing_card = False
                self.state = State.PLAYING
                print("PLAYING")
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
                self.showing_card = False  # SKIP
            return
        
        super().handle_events(keys)
        
        player_rect = self.player.get_rect()
        
        # Handle collision with solid objects
        for ob in self.objects:
            if ob.solid and player_rect.colliderect(ob.rect):
                if self.dx > 0:
                    player_rect.right = ob.rect.left
                elif self.dx < 0:
                    player_rect.left = ob.rect.right
                self.player.rect = player_rect
        
        # Handle enemy collision with objects
        for enemy in self.enemies:
            for ob in self.objects:
                if ob.solid and enemy.rect.colliderect(ob.rect):
                    if enemy.direction > 0:
                        enemy.rect.right = ob.rect.left
                    else:
                        enemy.rect.left = ob.rect.right
                    enemy.direction *= -1
    
    def draw(self):
        if self.state == State.GAME_OVER:
            return
        
        self.screen.fill(config.CLAY)
        
        if self.showing_card:
            self.draw_card()
            return
        
        if self.dialogue_triggered:
            self.dialogue.draw(self.screen)
        
        # Draw decorative borders
        self.draw_key_pattern(self.screen, self.meander_img, 
                            self.camera.offset_x * 0.5, 10)
        self.draw_key_pattern(self.screen, self.meander_img, 
                            self.camera.offset_x * 0.5, config.HEIGHT - 70)
        
        # Draw level-specific elements
        self.draw_level_elements()
        self.player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), self.player_rect_cam)

        # Draw enemies
        for enemy in self.enemies:
            enemy_rect_cam = self.camera.apply(enemy.rect)
            self.screen.blit(enemy.img, enemy_rect_cam)
        
        # Draw HUD
        self.draw_hud()
    
    def draw_level_elements(self):
        """Override this to draw level-specific objects (gates, walls, etc.)"""
        pass
    
    def draw_hud(self):
        """Draw the player's glory/stats"""
        font = pygame.font.Font("assets/Romanica.ttf", 12)
        glory_surf = font.render(f"GLORY: {self.player.glory}", True, config.BLACK)
        glory_rect = glory_surf.get_rect(topleft=(10, 4))
        self.screen.blit(glory_surf, glory_rect)
    
    def draw_card(self):
        """Draw the level intro card"""
        self.screen.fill(config.BLACK)
        self.card_sequence.draw(self.screen)
    
    def check_level_done(self):
        return self.state == State.RETURN
    
    def level_over(self):
        """Draw the level completion screen"""
        self.timer -= 1
        self.screen.fill(config.BLACK)
        
        big_font = pygame.font.Font("assets/Romanica.ttf", 36)
        small_font = pygame.font.Font("assets/Romanica.ttf", 24)
        
        # Title
        title_surf = big_font.render("VICTORY", True, config.CLAY)
        title_rect = title_surf.get_rect(center=(config.WIDTH // 2, 100))
        self.screen.blit(title_surf, title_rect)
        
        # Stats
        lines = self.get_completion_stats()
        start_y = 180
        line_spacing = 40
        
        for i, text in enumerate(lines):
            surf = small_font.render(text, True, config.CLAY)
            rect = surf.get_rect(center=(config.WIDTH // 2, start_y + i * line_spacing))
            self.screen.blit(surf, rect)
        
        # Continue hint
        if self.timer < 700:
            hint_surf = small_font.render("PRESS SPACE TO CONTINUE", True, config.CLAY)
            hint_rect = hint_surf.get_rect(center=(config.WIDTH // 2, config.HEIGHT - 80))
            self.screen.blit(hint_surf, hint_rect)
        
        if self.timer <= 0:
            self.state = State.RETURN
    
    def get_completion_stats(self):
        """Override this to customize completion screen stats"""
        return [
            f"{self.level_name} COMPLETE",
            f"GLORY: {self.player.glory}",
        ]
    
    def trigger_dialogue(self):
        """Start the dialogue sequence"""
        if not self.dialogue_triggered:
            self.dialogue.start()
            self.dialogue_triggered = True
    
    def draw_gate(self, surface, x_world, ground_y, label="ΜYΣΙΑ"):
        """Draw a decorative gate with collision detection"""
        GATE_COLOR = config.BLACK
        PILLAR_WIDTH = 40
        GATE_HEIGHT = 250
        GATE_WIDTH = 200
        BEAM_HEIGHT = 25
        
        # World-space rects
        left_pillar_world = pygame.Rect(x_world, ground_y - GATE_HEIGHT, 
                                       PILLAR_WIDTH, GATE_HEIGHT)
        right_pillar_world = pygame.Rect(x_world + GATE_WIDTH, ground_y - GATE_HEIGHT, 
                                        PILLAR_WIDTH, GATE_HEIGHT)
        beam_world = pygame.Rect(x_world, ground_y - GATE_HEIGHT - BEAM_HEIGHT,
                                GATE_WIDTH + PILLAR_WIDTH, BEAM_HEIGHT)
        
        # Camera-space rects for drawing
        left_pillar = self.camera.apply(left_pillar_world)
        right_pillar = self.camera.apply(right_pillar_world)
        beam = self.camera.apply(beam_world)
        
        # Draw pillars & beam
        pygame.draw.rect(surface, GATE_COLOR, left_pillar)
        
        # Draw player
        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)
        
        pygame.draw.rect(surface, GATE_COLOR, right_pillar)
        pygame.draw.rect(surface, GATE_COLOR, beam)
        
        # Label
        greek_font = pygame.font.Font("assets/FreeSerif.ttf", 20)
        label_surf = greek_font.render(label, True, config.CLAY)
        label_rect = label_surf.get_rect(center=(beam.centerx, beam.top + 10))
        surface.blit(label_surf, label_rect)
        
        # Collision detection for dialogue trigger
        passage_rect_world = pygame.Rect(
            x_world + PILLAR_WIDTH,
            ground_y - GATE_HEIGHT - BEAM_HEIGHT,
            GATE_WIDTH,
            GATE_HEIGHT + BEAM_HEIGHT,
        )
        
        if not self.dialogue_triggered and self.player.get_rect().colliderect(passage_rect_world):
            self.trigger_dialogue()