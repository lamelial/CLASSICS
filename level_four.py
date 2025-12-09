import pygame
import config
import random

from gameplay_level import GameplayLevel, State
from textfx import TextLine, TextSequence


class Villager(pygame.sprite.Sprite):
    """Fleeing civilians - not combatants"""

    def __init__(self, x, y):
        super().__init__()
        self.villager_img = pygame.image.load("assets/woman.png").convert_alpha()
        self.villager_img = pygame.transform.scale(self.villager_img, (int(self.villager_img.get_width() * 0.5), int(self.villager_img.get_height() * 0.5)))
        self.img = self.villager_img

        self.height = self.villager_img.get_height()
        self.rect = self.img.get_rect(topleft=(x, y))
        self.speed = 3
        self.fleeing = False
        
    def flee(self):
        """Villager runs away"""
        self.fleeing = True
        
    def update(self):
        if self.fleeing:
            self.rect.x -= self.speed  # Run left (away from player)

    def img(self):
        return self.img


class Building(pygame.sprite.Sprite):
    """Buildings that can be burned"""
    def __init__(self, x, y, villagers_inside=0):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 120
        self.height = 150
        self.burning = False
        self.burn_timer = 0
        self.burn_duration = 180  # frames
        self.villagers_inside = villagers_inside
        self.villagers_fled = False
        self.rect = pygame.Rect(x, y - self.height, self.width, self.height)
        self.solid = False
        
    def ignite(self):
        """Set building on fire"""
        if not self.burning:
            self.burning = True
            
    def update(self):
        if self.burning:
            self.burn_timer += 1
            
    def is_destroyed(self):
        return self.burning and self.burn_timer >= self.burn_duration


class LevelFour(GameplayLevel):

    def __init__(self, screen):
        super().__init__(screen, "LEVEL FOUR", "CUT OFF TROY'S SUPPLIES")

        self.buildings = pygame.sprite.Group()
        self.villagers = pygame.sprite.Group()
        self.buildings_burned = 0
        self.total_buildings = 6
        self.flame_particles = []
        self.civilians_flee_triggered = False

        self.setup_village()

    def setup_card_sequence(self):
        self.card_sequence.add_line(TextLine("CLEAR THE SETTLEMENTS", self.font, 100))
        self.card_sequence.add_line(TextLine("FOR HELEN", self.font, 100))

    def setup_dialogue(self):
        self.dialogue.add_line(TextLine("NO RESISTANCE...", self.font, 100, hold_frames=80))

    def setup_village(self):
        """Create buildings with villagers inside - no fighters"""
        building_positions = [600, 900, 1200, 1600, 2000, 2400]

        for x in building_positions:
            villagers_count = 2
            building = Building(x, config.GROUND_Y, villagers_count)
            self.buildings.add(building)
    
    def update(self):
        # Handle game over state
        if self.state == State.GAME_OVER:
            self.level_over()
            return

        # Handle card sequence
        if self.showing_card:
            self.card_sequence.update()
            if self.card_sequence.is_finished():
                self.showing_card = False
                self.state = State.PLAYING
                print("PLAYING")
            return

        # Update player and camera (like parent, but skip enemy check)
        self.player.update()
        self.camera.follow(self.player.get_rect(), config.GROUND_Y)

        # Update dialogue if active
        if self.dialogue_triggered:
            self.dialogue.update()
            if self.dialogue.is_finished():
                self.dialogue_triggered = False

        self.buildings.update()
        self.villagers.update()

        # Check for burning buildings near player
        player_rect = self.player.get_rect()
        
        for building in self.buildings:
            # Player collides with building = ignite it
            if not building.burning and player_rect.colliderect(building.rect):
                building.ignite()
                self.buildings_burned += 1
                
                # Spawn fleeing villagers
                if not building.villagers_fled:
                    building.villagers_fled = True
                    for i in range(building.villagers_inside):
                        villager = Villager(
                            building.x + (100 * i),
                            config.GROUND_Y - 250
                        )
                        villager.flee()
                        self.villagers.add(villager)

                    # Trigger dialogue first time civilians flee
                    if not self.civilians_flee_triggered:
                        self.civilians_flee_triggered = True
                        flee_dialogue = TextSequence(config.BLACK)
                        flee_dialogue.add_line(TextLine("CIVILIANS FLEE...", self.font, 100, hold_frames=80))
                        self.dialogue = flee_dialogue
                        self.trigger_dialogue()
        
        # Remove destroyed buildings
        for building in self.buildings:
            if building.is_destroyed():
                self.buildings.remove(building)
        
        # Remove villagers that fled off screen
        for villager in self.villagers:
            if villager.rect.right < 0:
                self.villagers.remove(villager)
        
        # Level ends when all buildings burned - no enemies to fight
        if len(self.buildings) == 0:
            self.state = State.GAME_OVER
    
    def draw_level_elements(self):
        """Draw buildings and fleeing villagers"""
        for building in self.buildings:
            self.draw_building(building)
        
        # Draw fleeing villagers
        for villager in self.villagers:
            villager_cam = self.camera.apply(villager.rect)
            self.screen.blit(villager.img, villager_cam)

    def draw_building(self, building):
        """Draw a building, with fire effects if burning"""
        BUILDING_COLOR = config.BLACK
        
        building_cam = self.camera.apply(building.rect)
        
        if building.burning:
            # Draw fire/smoke effect
            burn_progress = building.burn_timer / building.burn_duration
            
            # Building gets darker as it burns
            gray_value = int(255 * (1 - burn_progress))
            building_color = (gray_value, gray_value, gray_value)
            
            pygame.draw.rect(self.screen, building_color, building_cam, 3)
            
            # Simple fire effect - orange/red flickering
            if building.burn_timer % 10 < 5:
                fire_color = (255, 100, 0)  # Orange
            else:
                fire_color = (255, 50, 0)  # Red
            
            # Fire at top of building
            fire_rect = pygame.Rect(
                building_cam.left,
                building_cam.top - 20,
                building_cam.width,
                20
            )
            pygame.draw.rect(self.screen, fire_color, fire_rect)
        else:
            # Normal building
            pygame.draw.rect(self.screen, BUILDING_COLOR, building_cam, 3)
        
        # Roof
        roof_points = [
            (building_cam.left, building_cam.top),
            (building_cam.centerx, building_cam.top - 40),
            (building_cam.right, building_cam.top)
        ]
        pygame.draw.polygon(self.screen, BUILDING_COLOR, roof_points, 3)
    
    def draw_hud(self):
        """Use base dual messaging HUD"""
        # Call parent HUD (dual messaging)
        super().draw_hud()
    
    def get_completion_stats(self):
        """Clinical military report"""
        return [
            "SETTLEMENTS CLEARED",
            f"SPOILS TAKEN: {self.player.spoils}",
            "HELEN WAS NOT HERE",
        ]