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

        self.gate_x = 1200

        self.setup_enemies()
        self.state = State.PLAYING
        
    def setup_card_sequence(self):
        """Add level-specific narrative to the intro card"""
        self.card_sequence.add_line(TextLine("TROY'S ALLIES HOLD HELEN", self.font, 100))
        self.card_sequence.add_line(TextLine("TAKE LYRNESSUS", self.font, 100))
    
    def setup_dialogue(self):
        self.dialogue.add_line(TextLine("THE GATES OF LYRNESSUS...", self.font, 100, hold_frames=80))
    
    def setup_enemies(self):
        y_ground = config.GROUND_Y - 250
        start_x = config.WIDTH + 800

        for i in range(8):
            x = start_x + i * random.randint(180, 400)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
    
    def update(self):
        super().update()

        if not self.dialogue_triggered and self.player.get_rect().centerx > self.gate_x:
            self.trigger_dialogue()
    
    def draw_level_elements(self):
        self.draw_gate(self.screen, self.gate_x, config.GROUND_Y, label="ΛΥΡΝΗΣΣΌΣ")
            
    def get_completion_stats(self):
        """Darker victory message reflecting the sack of the city"""
        return [
            "LYRNESSUS HAS FALLEN",
            f"SPOILS TAKEN: {self.player.spoils}",
            "HELEN IS NOT HERE",
        ]

