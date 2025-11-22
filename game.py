import pygame
from enum import Enum
from level_one import LevelOne
from title_screen import TitleScreen
from intro import Intro

class State(Enum):
    TITLE = 0
    LEVEL = 1
    CUT = 2


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.state = State.TITLE
        self.level_index = 0
        self.current_level = None
        self.levels = [Intro(self.screen), LevelOne(self.screen)]
        self.title_screen = TitleScreen(self.screen)

    def start_level(self, index):
        self.level_index = index
        self.current_level = self.levels[index]
        self.state = State.LEVEL

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if self.state == State.TITLE or self.state == State.CUT:
            if any(keys):
                self.start_level(self.level_index)

        elif self.state == State.LEVEL:
            self.current_level.handle_events(keys)

    def update(self):
        if self.state == State.LEVEL:
            self.current_level.update()
            if self.current_level.check_level_done():
                self.state = State.CUT
                self.current_level = None
                self.level_index += 1

    def draw(self):
        if self.state == State.TITLE:
            self.title_screen.draw_title()
        elif self.state == State.LEVEL:
            self.current_level.draw()
        elif self.state == State.CUT:
            self.title_screen.draw_agam()
