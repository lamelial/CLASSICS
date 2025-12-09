import pygame
import config
import random

from gameplay_level import GameplayLevel, State
from enemy import Enemy
from textfx import TextLine
from textfx import TextSequence


class LevelOne(GameplayLevel):
    """Level One: The Attack on Mysia - The Greeks attack the wrong city entirely"""
    
    def __init__(self, screen):
        super().__init__(screen, "LEVEL ONE", "LANDFALL AT TROY")

        self.gate_x = 1200
        self.setup_enemies()
        self.state = State.PLAYING
        
    def setup_card_sequence(self):
        self.card_sequence.add_line(TextLine("HELEN AWAITS", self.font, 80))
        self.card_sequence.add_line(TextLine("BREACH THE GATES", self.font, 100))
    
    def setup_dialogue(self):
        self.dialogue.add_line(TextLine("THE GATES OF MYSIA...", self.font, 100, hold_frames=80))
    
    def setup_enemies(self):
        y_ground = config.GROUND_Y - 250
        start_x = config.WIDTH + 800
        
        for i in range(6):
            x = start_x + i * random.randint(180, 400)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
    
    def update(self):
        super().update()

        # Trigger dialogue when player reaches the gate
        if not self.dialogue_triggered and self.player.get_rect().centerx > self.gate_x:
            self.trigger_dialogue()
    
    def draw_level_elements(self):
        # The gate is labeled ΜYΣΙΑ but the player was told this is Troy
        self.draw_gate(self.screen, self.gate_x, config.GROUND_Y, label="ΜYΣΙΑ")
    
    def get_completion_stats(self):
        return [
            "MYSIA HAS FALLEN",
            "THE WRONG CITY",
            f"SPOILS TAKEN: {self.player.spoils}",
            f"GLORY EARNED: {self.player.spoils / 2:.0f}",
            "HELEN IS NOT HERE",
        ]


