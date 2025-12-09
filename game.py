import pygame
from enum import Enum
from level_one import LevelOne
from level_two import LevelTwo
from level_three import LevelThree
from level_four import LevelFour
from level_five import LevelFive 
from card import Card
from intro import Intro

class State(Enum):
    TITLE = 0
    LEVEL = 1


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.state = State.TITLE
        self.level_index = 0
        self.current_level = None
        self.levels = [Intro(self.screen), LevelOne(self.screen), LevelTwo(self.screen), LevelThree(self.screen), LevelFour(self.screen), LevelFive(self.screen)]
        self.title_screen = Card(self.screen)

    def start_level(self, index):
        self.level_index = index
        self.current_level = self.levels[index]
        self.state = State.LEVEL

    def handle_events(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if self.state == State.TITLE:
            if any(keys):
                self.start_level(self.level_index)
        # dev tools
        if keys[pygame.K_1]:
            self.start_level(1)
        if keys[pygame.K_2]:
            self.start_level(2)
        if keys[pygame.K_3]:
            self.start_level(3)
        if keys[pygame.K_4]:
            self.start_level(4)
        if keys[pygame.K_5]:
            self.start_level(5)

        elif self.state == State.LEVEL:
            self.current_level.handle_events(keys, mouse_buttons)

    def update(self):
        if self.state == State.LEVEL:
            self.current_level.update()
            if self.current_level.check_level_done():
                # Go directly to next level (no cutscene)
                if self.level_index < len(self.levels) - 1:
                    self.level_index += 1
                    self.start_level(self.level_index)
                else:
                    # Game finished - return to title
                    self.state = State.TITLE
                    self.level_index = 0

    def draw(self):
        if self.state == State.TITLE:
            self.title_screen.draw_title()
        elif self.state == State.LEVEL:
            self.current_level.draw()
