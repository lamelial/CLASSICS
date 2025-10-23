import pygame


class Player(pygame.sprite.Sprite):
    _SPEED = 5
    _IMG_PATH = "assets/achilles.png"
    _JUMP_STRENGTH = -15

    def __init__(self, x, y):
        super().__init__()
        self.forward_img = pygame.transform.scale(pygame.image.load(self._IMG_PATH).convert_alpha(), (int(80 * 1.5), int(120 * 1.5)))
        self.backward_img = pygame.transform.flip(self.forward_img, True, False)
        self.img = self.forward_img
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
            self.img = self.forward_img
        elif dx < 0:
            self.facing_right = False
            self.img = self.backward_img

    def update(self, gravity, ground_y):
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True

    def get_rect(self):
        return self.rect

    def get_img(self):
        return self.img
