import pygame
import config
import random

from gameplay_level import GameplayLevel, State
from enemy import Enemy
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


class LevelThree(GameplayLevel):
    """Level Three: Scorched Earth - Burn villages, watch civilians flee"""
    
    def __init__(self, screen):
        super().__init__(screen, "LEVEL THREE", "SCORCHED EARTH PROTOCOL")
        
        self.buildings = pygame.sprite.Group()
        self.villagers = pygame.sprite.Group()
        self.buildings_burned = 0
        self.total_buildings = 6
        self.flame_particles = []
        
        self.setup_village()
        self.setup_enemies()
        
    def setup_card_sequence(self):
        """Military language for burning villages"""
        self.card_sequence.add_line(TextLine("DENYING RESOURCES TO THE ENEMY", self.font, 100))
        self.card_sequence.add_line(TextLine("ELIMINATE SUPPLY INFRASTRUCTURE", self.font, 100))
        self.card_sequence.add_line(TextLine("ACCEPTABLE CIVILIAN IMPACT", self.font, 100))
    
    def setup_dialogue(self):
        """The orders are clear, but uncomfortable"""
        self.dialogue.add_line(TextLine("THE VILLAGE OF PEDASUS", self.font, 100, hold_frames=50))
        self.dialogue.add_line(TextLine("THEY FEED TROY'S ARMIES", self.font, 100, hold_frames=60))
        self.dialogue.add_line(TextLine("BURN IT ALL", self.font, 100, hold_frames=80))
    
    def setup_village(self):
        """Create buildings with villagers inside"""
        building_positions = [600, 900, 1200, 1600, 2000, 2400]
        
        for x in building_positions:
            villagers_count = random.randint(2, 4)
            building = Building(x, config.GROUND_Y, villagers_count)
            self.buildings.add(building)
    
    def setup_enemies(self):
        """A few defenders - mostly it's just civilians"""
        y_ground = config.GROUND_Y - 250
        
        # Only a handful of actual fighters
        for i in range(4):
            x = 800 + i * random.randint(300, 500)
            enemy = Enemy(x, y_ground)
            self.enemies.add(enemy)
    
    def update(self):
        super().update()
        
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
                            building.x + random.randint(0, 150),
                            config.GROUND_Y - 250
                        )
                        villager.flee()
                        self.villagers.add(villager)
        
        # Remove destroyed buildings
        for building in self.buildings:
            if building.is_destroyed():
                self.buildings.remove(building)
        
        # Remove villagers that fled off screen
        for villager in self.villagers:
            if villager.rect.right < 0:
                self.villagers.remove(villager)
        
        # Level ends when all buildings burned and enemies dead
        if len(self.buildings) == 0 and len(self.enemies) == 0:
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
        """Show progress of destruction"""
        font = pygame.font.Font("assets/Romanica.ttf", 12)
        
        # Show as "objectives completed"
        hud_text = f"STRUCTURES ELIMINATED: {self.buildings_burned}/{self.total_buildings}"
        hud_surf = font.render(hud_text, True, config.BLACK)
        hud_rect = hud_surf.get_rect(topleft=(10, 4))
        self.screen.blit(hud_surf, hud_rect)
        
        # Glory counter below
        glory_surf = font.render(f"GLORY: {self.player.glory}", True, config.BLACK)
        glory_rect = glory_surf.get_rect(topleft=(10, 20))
        self.screen.blit(glory_surf, glory_rect)
    
    def get_completion_stats(self):
        """Clinical military report"""
        return [
            "VILLAGE PACIFIED",
            f"GLORY: {self.player.glory}",
            f"STRUCTURES DESTROYED: {self.total_buildings}",
            "DISPLACED CIVILIANS: MULTIPLE",
            "MISSION: ACCOMPLISHED",
        ]