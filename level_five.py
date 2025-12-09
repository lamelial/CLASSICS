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

    def update(self):
        # Simple movement - flee left
        self.rect.x -= self.speed


class BurningHouse(pygame.sprite.Sprite):
    """A burning building in Troy"""
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.flame_offset = random.randint(0, 60)

    def draw(self, surface, camera):
        # Draw house structure
        house_cam = camera.apply(self.rect)
        pygame.draw.rect(surface, config.BLACK, house_cam, 3)

        # Draw flames on top
        flame_height = 20 + abs(int(10 * pygame.time.get_ticks() / 100 % 10 - 5))
        flame_y = house_cam.top - flame_height

        # Multiple flame points
        for i in range(3):
            flame_x = house_cam.left + (i + 1) * (self.width // 4)
            flame_points = [
                (flame_x, flame_y),
                (flame_x - 10, house_cam.top),
                (flame_x + 10, house_cam.top)
            ]
            pygame.draw.polygon(surface, config.RED, flame_points)


class LevelFive(GameplayLevel):
    """Level Five: The Sack of Troy"""

    def __init__(self, screen):
        super().__init__(screen, "LEVEL FIVE", "THE SACK OF TROY")

        self.gate_x = 1500
        self.passed_gate = False
        self.gate_message_shown = False

        self.civilians = pygame.sprite.Group()
        self.houses = []

        self.setup_troy()
        self.setup_enemies()

    def setup_card_sequence(self):
        """Opening cards"""
        self.card_sequence.add_line(TextLine("TEN YEARS", self.font, 100))
        self.card_sequence.add_line(TextLine("AT LAST: TROY", self.font, 100))
        self.card_sequence.add_line(TextLine("RESCUE HELEN", self.font, 100))

    def setup_dialogue(self):
        """Gate message"""
        self.dialogue.add_line(TextLine("THE WALLS OF TROY", self.font, 100, hold_frames=80))

    def setup_troy(self):
        """Setup burning houses and fleeing civilians"""
        y_ground = config.GROUND_Y

        # Create burning houses beyond the gate
        house_positions = [
            (self.gate_x + 200, y_ground - 150, 120, 150),
            (self.gate_x + 400, y_ground - 180, 100, 180),
            (self.gate_x + 600, y_ground - 140, 130, 140),
            (self.gate_x + 850, y_ground - 160, 110, 160),
            (self.gate_x + 1100, y_ground - 170, 140, 170),
        ]

        for x, y, w, h in house_positions:
            house = BurningHouse(x, y, w, h)
            self.houses.append(house)

        # Create fleeing civilians
        for i in range(15):
            x = self.gate_x + random.randint(150, 1000)
            y = y_ground - random.randint(240, 260)
            civilian = TrojanCivilian(x, y)
            self.civilians.add(civilian)

    def setup_enemies(self):
        """Enemies scattered throughout Troy"""
        y_ground = config.GROUND_Y - 250

        # Enemies inside Troy
        for i in range(12):
            x = self.gate_x + random.randint(200, 1200)
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

        # Show gate message when player walks through
        if not self.gate_message_shown and player_x > self.gate_x - 50:
            self.gate_message_shown = True
            self.dialogue_triggered = True
            self.passed_gate = True

        # Update civilians
        self.civilians.update()

        # Remove civilians that fled off screen
        for civilian in list(self.civilians):
            if civilian.rect.right < -100:
                self.civilians.remove(civilian)

        # Update dialogue
        if self.dialogue_triggered:
            self.dialogue.update()
            if self.dialogue.is_finished():
                self.dialogue_triggered = False

        # Level ends when all enemies are defeated
        if len(self.enemies) == 0:
            self.state = State.GAME_OVER

    def draw_level_elements(self):
        """Draw Troy's gate, burning houses, and fleeing civilians"""
        self.draw_gate(self.screen, self.gate_x, config.GROUND_Y)

        # Draw burning houses
        for house in self.houses:
            house.draw(self.screen, self.camera)

        # Draw fleeing civilians
        for civilian in self.civilians:
            civilian_cam = self.camera.apply(civilian.rect)
            self.screen.blit(civilian.img, civilian_cam)

    def draw_gate(self, surface, x_world, ground_y):
        """Draw the gate/walls of Troy"""
        WALL_COLOR = config.BLACK

        wall_height = 350
        wall_width = 100

        # Left wall
        wall_world = pygame.Rect(x_world - 60, ground_y - wall_height, wall_width, wall_height)
        wall_cam = self.camera.apply(wall_world)
        pygame.draw.rect(surface, WALL_COLOR, wall_cam, 5)

        # Right wall
        wall_world2 = pygame.Rect(x_world + 60, ground_y - wall_height, wall_width, wall_height)
        wall_cam2 = self.camera.apply(wall_world2)
        pygame.draw.rect(surface, WALL_COLOR, wall_cam2, 5)

        # Gate opening
        gate_world = pygame.Rect(x_world - 50, ground_y - 220, 100, 220)
        gate_cam = self.camera.apply(gate_world)
        pygame.draw.rect(surface, WALL_COLOR, gate_cam, 4)

        # Battlements on top
        for i in range(15):
            battlement_world = pygame.Rect(
                x_world - 60 + i * 20,
                ground_y - wall_height - 25,
                15, 25
            )
            battlement_cam = self.camera.apply(battlement_world)
            pygame.draw.rect(surface, WALL_COLOR, battlement_cam)

    def draw_hud(self):
        """Use base HUD"""
        super().draw_hud()

    def get_completion_stats(self):
        """Completion message"""
        return [
            "TROY HAS FALLEN",
            "",
            f"TOTAL SPOILS: {self.player.spoils}",
            "",
            "HELEN WAS NOT HERE",
            "",
            "SHE WAS NEVER HERE",
        ]
