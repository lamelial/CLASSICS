import pygame

class Player:
    _SPEED = 5
    _IMG_PATH = "assets/achilles.png"
    _JUMP_STRENGTH = -15

    def __init__(self, x, y):
        self.img = pygame.image.load(self._IMG_PATH).convert_alpha()
        self.img = pygame.transform.scale(self.img, (int(80 * 1.5), int(120 * 1.5)))
        self.rect = self.img.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = True
        self.facing_right = True

    def jump(self):
        if self.on_ground:
            self.vel_y = self._JUMP_STRENGTH
            self.on_ground = False

    def move(self, dx):
        self.rect.x += dx * self._SPEED
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

    def update(self, gravity, ground_y):
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True

    def draw(self, surface):
        surface.blit(self.img, self.rect)

    def get_rect(self):
        return self.rect

    def get_img(self):
        return self.img
