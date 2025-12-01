import pygame
import config
import random

from gameplay_level import GameplayLevel
from gameplay_level import State
from enemy import Enemy
from textfx import TextLine
from textfx import TextSequence


class LevelTwo(GameplayLevel):
    def __init__(self, screen):
        super().__init__(screen, "LEVEL TWO", "THE SIEGE OF LYRNESSUS")
        
        # Multiple gates representing the city's defenses
        self.gate_positions = [800, 1600, 2400]
        self.current_gate_index = 0
        self.gates_breached = 0
        
        # City background elements
        self.tower_img = None  # Can add tower graphics if you have them
        
        self.setup_enemies()
        
    def setup_card_sequence(self):
        """Add level-specific narrative to the intro card"""
        self.card_sequence.add_line(TextLine("TO WEAKEN TROY, WE MUST TAKE HER ALLIES", self.font, 100))
        self.card_sequence.add_line(TextLine("SACK THE CITY OF LYRNESSUS", self.font, 100))
    
    def setup_dialogue(self):
        """Set up dialogue for each gate"""
        # First gate
        self.dialogue_gate_1 = TextSequence(config.BLACK)
        self.dialogue_gate_1.add_line(TextLine("THE GATES OF LYRNESSUS", self.font, 100, hold_frames=50))
        
        # Second gate 
        self.dialogue_gate_2 = TextSequence(config.BLACK)
        self.dialogue_gate_2.add_line(TextLine("KING MYNES DEFENDS HIS CITY", self.font, 100, hold_frames=50))
        
        # Third gate (final)
        self.dialogue_gate_3 = TextSequence(config.BLACK)
        self.dialogue_gate_3.add_line(TextLine("THE TEMPLE OF APOLLO", self.font, 100, hold_frames=50))
        self.dialogue_gate_3.add_line(TextLine("THE CITY FALLS...", self.font, 100, hold_frames=50))
        
        self.dialogue = self.dialogue_gate_1
    
    def setup_enemies(self):
        """Spawn waves of enemies at each gate"""
        y_ground = config.GROUND_Y - 250
        
        # Wave 1: Light defenders
        for i in range(3):
            x = self.gate_positions[0] + 100 + i * random.randint(150, 300)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
        
        # Wave 2: Main force with King Mynes (stronger enemies)
        for i in range(5):
            x = self.gate_positions[1] + 100 + i * random.randint(150, 300)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
        
        # Wave 3: Temple guards (final defense)
        for i in range(4):
            x = self.gate_positions[2] + 100 + i * random.randint(150, 300)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
    
    def update(self):
        super().update()
        
        # Check if player has passed each gate
        if self.state == State.PLAYING and not self.dialogue_triggered:
            player_x = self.player.get_rect().centerx
            
            # Check gate progression
            if self.gates_breached == 0 and player_x > self.gate_positions[0] + 150:
                self.gates_breached = 1
            elif self.gates_breached == 1 and player_x > self.gate_positions[1] + 150:
                self.gates_breached = 2
            elif self.gates_breached == 2 and player_x > self.gate_positions[2] + 150:
                self.gates_breached = 3
    
    def draw_level_elements(self):
        """Draw multiple gates representing the city's defenses"""
        labels = ["ΛΥΡΝΗΣΣΌΣ", "ΜΥΝΗΣ", "ΑΠΌΛΛΩΝ"]
        
        for i, gate_x in enumerate(self.gate_positions):
            if i < len(labels):
                self.draw_gate(self.screen, gate_x, config.GROUND_Y, labels[i])
    
    def draw_gate(self, surface, x_world, ground_y, label="ΛΥΡΝΗΣΣΌΣ"):
        """Draw a gate with custom collision for dialogue"""
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
        
        # Draw player (only once, on first gate)
        if x_world == self.gate_positions[0]:
            player_rect_cam = self.camera.apply(self.player.get_rect())
            self.screen.blit(self.player.get_img(), player_rect_cam)
        
        pygame.draw.rect(surface, GATE_COLOR, right_pillar)
        pygame.draw.rect(surface, GATE_COLOR, beam)
        
        # Label
        greek_font = pygame.font.Font("assets/FreeSerif.ttf", 20)
        label_surf = greek_font.render(label, True, config.CLAY)
        label_rect = label_surf.get_rect(center=(beam.centerx, beam.top + 10))
        surface.blit(label_surf, label_rect)
        
        # Collision detection for dialogue
        passage_rect_world = pygame.Rect(
            x_world + PILLAR_WIDTH,
            ground_y - GATE_HEIGHT - BEAM_HEIGHT,
            GATE_WIDTH,
            GATE_HEIGHT + BEAM_HEIGHT,
        )
        
        if not self.dialogue_triggered and self.player.get_rect().colliderect(passage_rect_world):
            # Determine which gate we're at and trigger appropriate dialogue
            if x_world == self.gate_positions[0] and self.current_gate_index == 0:
                self.dialogue = self.dialogue_gate_1
                self.trigger_dialogue()
                self.current_gate_index = 1
            elif x_world == self.gate_positions[1] and self.current_gate_index == 1:
                self.dialogue = self.dialogue_gate_2
                self.trigger_dialogue()
                self.current_gate_index = 2
            elif x_world == self.gate_positions[2] and self.current_gate_index == 2:
                self.dialogue = self.dialogue_gate_3
                self.trigger_dialogue()
                self.current_gate_index = 3
    
    def get_completion_stats(self):
        """Darker victory message reflecting the sack of the city"""
        return [
            "LYRNESSUS HAS FALLEN",
            f"GLORY: {self.player.glory}",
            "THE SPOILS OF WAR ARE OURS",
            "BUT AT WHAT COST...",
        ]

