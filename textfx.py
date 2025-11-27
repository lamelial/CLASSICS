# textfx.py
import pygame
import config


class TextLine:
    """
    One line of text that can fade in, hold, then fade out.
    """
    def __init__(self, text, font, y,
                 fade_in_speed=5,
                 hold_frames=90,
                 fade_out_speed=5):
        self.text = text
        self.font = font
        self.y = y

        self.fade_in_speed = fade_in_speed
        self.hold_frames = hold_frames
        self.fade_out_speed = fade_out_speed

        self.alpha = 0
        self.state = "FADE_IN"   # FADE_IN -> HOLD -> FADE_OUT -> DONE
        self.timer = hold_frames
        self.done = False

    def update(self):
        if self.done:
            return

        if self.state == "FADE_IN":
            self.alpha += self.fade_in_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.state = "HOLD"

        elif self.state == "HOLD":
            self.timer -= 1
            if self.timer <= 0:
                self.state = "FADE_OUT"

        elif self.state == "FADE_OUT":
            self.alpha -= self.fade_out_speed
            if self.alpha <= 0:
                self.alpha = 0
                self.done = True

    def draw(self, surface, color=(0, 0, 0)):
        if self.done:
            return
        surf = self.font.render(self.text, True, color)
        surf.set_alpha(self.alpha)
        rect = surf.get_rect(center=(config.WIDTH // 2, self.y))
        surface.blit(surf, rect)


class TextSequence:
    """
    Plays several TextLine objects one after another.
    """
    def __init__(self, color=config.BLACK):
        self.lines = []
        self.current_index = 0
        self.active = False
        self.finished = False
        self.color = color

    def add_line(self, line: TextLine):
        self.lines.append(line)

    def start(self):
        if self.lines:
            self.active = True
            self.finished = False
            self.current_index = 0

    def update(self):
        if not self.active or self.finished or not self.lines:
            return

        current = self.lines[self.current_index]
        current.update()

        if current.done:
            self.current_index += 1
            if self.current_index >= len(self.lines):
                self.finished = True
                self.active = False

    def draw(self, surface):
        if not self.active or self.finished or not self.lines:
            return
        self.lines[self.current_index].draw(surface, self.color)

    def is_finished(self):
        return self.finished


