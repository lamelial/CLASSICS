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
        self.revelation_triggered = False
        self.setup_enemies()
        self.state = State.PLAYING
        
    def setup_card_sequence(self):
        self.card_sequence.add_line(TextLine("WE HAVE ARRIVED TO RESCUE HELEN", self.font, 100))
        self.card_sequence.add_line(TextLine("(AND CLAIM TROY'S RICHES)", self.font, 80))
        self.card_sequence.add_line(TextLine("BREACH THE GATES", self.font, 100))
    
    def setup_dialogue(self):
        """The uncomfortable revelation - this isn't Troy at all"""
        self.dialogue_gate = TextSequence(config.BLACK)
        self.dialogue_gate.add_line(TextLine("THE GATES OF TROY...", self.font, 100, hold_frames=60))
        
        self.dialogue_revelation = TextSequence(config.BLACK)
        self.dialogue_revelation.add_line(TextLine("WAIT.", self.font, 100, hold_frames=40))
        self.dialogue_revelation.add_line(TextLine("MYSIA.", self.font, 100, hold_frames=60))
        self.dialogue_revelation.add_line(TextLine("WE CAME TO THE WRONG PLACE.", self.font, 100, hold_frames=100))
        
        self.dialogue = self.dialogue_gate
    
    def setup_enemies(self):
        y_ground = config.GROUND_Y - 250
        start_x = config.WIDTH + 800
        
        for i in range(6):
            x = start_x + i * random.randint(180, 400)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
    
    def update(self):
        player_x = self.player.get_rect().centerx
        trigger_x = self.gate_x + 300
        super().update()

        print(f"Player X: {player_x}, Trigger X: {trigger_x}, State: {self.state}, Rev Triggered: {self.revelation_triggered}, Dialogue Triggered: {self.dialogue_triggered}")
        print(self.state)
        if (self.state == State.PLAYING and not self.revelation_triggered and self.player.get_rect().centerx > self.gate_x + 1000):
            self.revelation_triggered = True
            self.dialogue = self.dialogue_revelation
            self.dialogue.start()
            self.dialogue_triggered = True
    
    def draw_level_elements(self):
        """Draw the gate labeled as 'Mysia' - but the player thinks it's Troy"""
        # The gate is labeled ΜYΣΙΑ but the player was told this is Troy
        self.draw_gate(self.screen, self.gate_x, config.GROUND_Y, label="ΜYΣΙΑ")
    
    def get_completion_stats(self):
        """Victory screen with an uncomfortable truth"""
        return [
            "MYSIA HAS FALLEN",
            f"GLORY: {self.player.glory}",
            "BUT THIS WAS NOT TROY...",
            "HELEN WAS NEVER HERE",
        ]


