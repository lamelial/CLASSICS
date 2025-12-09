import pygame
import config
import random

from gameplay_level import GameplayLevel, State
from enemy import Enemy
from textfx import TextLine, TextSequence


class Civilian(pygame.sprite.Sprite):
    """Fleeing civilians - more than in Level 3"""
    def __init__(self, x, y, size="adult"):
        super().__init__()
        # Load woman sprite for all civilians
        base_img = pygame.image.load("assets/woman.png").convert_alpha()
        
        if size == "child":
            scale = 0.3
        else:
            scale = 0.5
            
        self.img = pygame.transform.scale(
            base_img, 
            (int(base_img.get_width() * scale), int(base_img.get_height() * scale))
        )
        
        self.rect = self.img.get_rect(topleft=(x, y))
        self.speed = 2 if size == "child" else 3
        self.fleeing = False
        self.panic_radius = 350  # Start fleeing when player gets this close
        
    def update_fleeing(self, player_x):
        # Flee when player approaches
        if not self.fleeing and abs(self.rect.centerx - player_x) < self.panic_radius:
            self.fleeing = True
            
        if self.fleeing:
            self.rect.x -= self.speed


class LevelFour(GameplayLevel):
    """Level Four: Escalation - More fleeing, children running, chaos"""
    
    def __init__(self, screen):
        super().__init__(screen, "LEVEL FOUR", "SECURE THE REGION")
        
        self.civilians = pygame.sprite.Group()
        self.city_positions = [800, 1400, 2000]
        self.initial_civilian_count = 0
        
        self.setup_civilians()
        self.setup_enemies()
        
    def setup_card_sequence(self):
        """Vague military objectives"""
        self.card_sequence.add_line(TextLine("CLEAR THE SETTLEMENTS", self.font, 100))
        self.card_sequence.add_line(TextLine("FOR HELEN", self.font, 100))
    
    def setup_dialogue(self):
        """Just cold orders"""
        self.dialogue.add_line(TextLine("CLEAR THE SETTLEMENTS", self.font, 100, hold_frames=60))
    
    def setup_civilians(self):
        """Lots of civilians - including children"""
        for city_x in self.city_positions:
            # Each settlement has families
            for i in range(random.randint(5, 8)):
                x = city_x + random.randint(-150, 150)
                y = config.GROUND_Y - 250
                
                # Some children, some adults
                if random.random() < 0.3:
                    civilian = Civilian(x, y, "child")
                else:
                    civilian = Civilian(x, y, "adult")
                    
                self.civilians.add(civilian)
        
        self.initial_civilian_count = len(self.civilians)
    
    def setup_enemies(self):
        """Fewer actual soldiers than civilians"""
        y_ground = config.GROUND_Y - 250
        
        # Scattered, desperate defenders
        for i in range(6):
            x = 600 + i * random.randint(200, 400)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
    
    def update(self):
        # Don't call super().update() yet - we need to handle civilians first
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
        
        # Update civilians with player position
        player_x = self.player.get_rect().centerx
        for civilian in self.civilians:
            civilian.update_fleeing(player_x)
            
            # Remove if fled off screen
            if civilian.rect.right < 0:
                self.civilians.remove(civilian)
        
        # Level ends when all enemies dead
        if len(self.enemies) == 0:
            self.state = State.GAME_OVER
        
        if self.dialogue_triggered:
            self.dialogue.update()
            if self.dialogue.is_finished():
                self.dialogue_triggered = False
    
    def draw_level_elements(self):
        """Draw simple settlements and fleeing masses"""
        # Draw settlement markers
        for x in self.city_positions:
            self.draw_settlement(x)
        
        # Draw all the fleeing civilians
        for civilian in self.civilians:
            civilian_cam = self.camera.apply(civilian.rect)
            self.screen.blit(civilian.img, civilian_cam)
    
    def draw_settlement(self, x_world):
        """Simple settlement marker"""
        marker_world = pygame.Rect(x_world, config.GROUND_Y - 100, 80, 100)
        marker_cam = self.camera.apply(marker_world)
        pygame.draw.rect(self.screen, config.BLACK, marker_cam, 2)
    
    def draw_hud(self):
        """Use base dual messaging HUD"""
        # Call parent HUD (dual messaging)
        super().draw_hud()
    
    def get_completion_stats(self):
        """Clinical and brief"""
        return [
            "SETTLEMENTS CLEARED",
            f"SPOILS TAKEN: {self.player.spoils}",
            "HELEN WAS NOT HERE",
        ]