import pygame
import config
import random

from gameplay_level import GameplayLevel, State
from enemy import Enemy
from textfx import TextLine, TextSequence


class TrojanCivilian(pygame.sprite.Sprite):
    """Trojan civilians fleeing the sack"""
    def __init__(self, x, y):
        super().__init__()
        base_img = pygame.image.load("assets/woman.png").convert_alpha()
        self.img = pygame.transform.scale(
            base_img,
            (int(base_img.get_width() * 0.5), int(base_img.get_height() * 0.5))
        )
        self.rect = self.img.get_rect(topleft=(x, y))
        self.speed = random.randint(2, 4)
        self.fleeing = True
        
    def update(self):
        if self.fleeing:
            self.rect.x -= self.speed
            self.rect.y += random.randint(-1, 1)


class LevelFive(GameplayLevel):
    """Level Five: The Sack of Troy - Maximum chaos, Helen absent, maximum glory"""
    
    def __init__(self, screen):
        super().__init__(screen, "LEVEL FIVE", "OPERATION: HELEN")
        
        self.troy_gates_x = 1500
        self.gates_breached = False
        self.trojans = pygame.sprite.Group()
        self.mission_bonus = 500
        
        self.setup_enemies()
        
    def setup_card_sequence(self):
        """Back to the original, simple mission"""
        self.card_sequence.add_line(TextLine("TEN YEARS", self.font, 100))
        self.card_sequence.add_line(TextLine("AT LAST: TROY", self.font, 100))
        self.card_sequence.add_line(TextLine("RESCUE HELEN", self.font, 100))
    
    def setup_dialogue(self):
        """Just the objective at the gates"""
        self.dialogue.add_line(TextLine("FIND HELEN", self.font, 100, hold_frames=60))
    
    def setup_enemies(self):
        """Massive final battle"""
        y_ground = config.GROUND_Y - 250
        
        # Dense defenders
        start_x = config.WIDTH + 300
        for i in range(18):
            x = start_x + i * random.randint(120, 280)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
    
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
        
        player_x = self.player.get_rect().centerx
        
        # Gates breach when player reaches them
        if not self.gates_breached and player_x > self.troy_gates_x - 50:
            self.gates_breached = True
            self.spawn_fleeing_trojans()
        
        # Update fleeing Trojans
        self.trojans.update()
        
        # Remove those who fled off screen
        for trojan in self.trojans:
            if trojan.rect.right < -100:
                self.trojans.remove(trojan)
        
        # Level ends when all enemies dead
        if len(self.enemies) == 0:
            self.state = State.GAME_OVER
        
        if self.dialogue_triggered:
            self.dialogue.update()
            if self.dialogue.is_finished():
                self.dialogue_triggered = False
    
    def spawn_fleeing_trojans(self):
        """When gates breach, masses flee"""
        for i in range(25):
            x = self.troy_gates_x + random.randint(100, 700)
            y = config.GROUND_Y - random.randint(240, 260)
            trojan = TrojanCivilian(x, y)
            self.trojans.add(trojan)
    
    def draw_level_elements(self):
        """Draw Troy's walls and the chaos inside"""
        self.draw_troy_walls(self.screen, self.troy_gates_x, config.GROUND_Y)
        
        # Draw fleeing Trojans
        for trojan in self.trojans:
            trojan_cam = self.camera.apply(trojan.rect)
            self.screen.blit(trojan.img, trojan_cam)
    
    def draw_troy_walls(self, surface, x_world, ground_y):
        """Troy's massive walls"""
        WALL_COLOR = config.BLACK
        
        wall_height = 350
        wall_width = 100
        wall_world = pygame.Rect(x_world, ground_y - wall_height, wall_width, wall_height)
        wall_cam = self.camera.apply(wall_world)
        pygame.draw.rect(surface, WALL_COLOR, wall_cam, 5)
        
        if self.gates_breached:
            # Gates smashed
            gate_world = pygame.Rect(x_world + 25, ground_y - 200, 50, 200)
            gate_cam = self.camera.apply(gate_world)
            # Broken pieces
            pygame.draw.rect(surface, WALL_COLOR, 
                           pygame.Rect(gate_cam.left - 25, gate_cam.bottom - 50, 30, 50), 3)
            pygame.draw.rect(surface, WALL_COLOR,
                           pygame.Rect(gate_cam.right + 15, gate_cam.bottom - 40, 30, 40), 3)
        else:
            # Intact gate
            gate_world = pygame.Rect(x_world + 25, ground_y - 220, 50, 220)
            gate_cam = self.camera.apply(gate_world)
            pygame.draw.rect(surface, WALL_COLOR, gate_cam, 4)
        
        # Battlements
        for i in range(10):
            battlement_world = pygame.Rect(
                x_world + i * 30, 
                ground_y - wall_height - 25, 
                20, 25
            )
            battlement_cam = self.camera.apply(battlement_world)
            pygame.draw.rect(surface, WALL_COLOR, battlement_cam)
        
        # TROY label
        greek_font = pygame.font.Font("assets/FreeSerif.ttf", 32)
        label_surf = greek_font.render("ΤΡΟΊΑ", True, config.CLAY)
        label_x = wall_cam.centerx - label_surf.get_width() // 2
        label_y = wall_cam.centery
        surface.blit(label_surf, (label_x, label_y))
    
    def draw_hud(self):
        """Use base dual messaging HUD"""
        # Call parent HUD (dual messaging)
        super().draw_hud()
    
    def get_completion_stats(self):
        """MASSIVE glory reward, Helen absent, no commentary"""
        return [
            "TROY HAS FALLEN",
            "",
            f"TOTAL SPOILS: {self.player.spoils}",
            "",
            "HELEN WAS NOT HERE",
            "",
            "SHE WAS NEVER HERE",
        ]