import pygame


class Boat(pygame.sprite.Sprite):
    _SPEED = 5
    _IMG_PATH = "assets/boat.png"
    _JUMP_STRENGTH = -15

    def __init__(self, x, y):
        super().__init__()
        self.img = pygame.transform.scale(pygame.image.load(self._IMG_PATH).convert_alpha(), (int(758 * 0.5), int(534 * 0.5)))
        self.img = pygame.transform.flip(self.img, True, False)
        self.rect = self.img.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = True
        self.facing_right = True

    def move(self, dx):
        self.rect.x += dx * self._SPEED

    def update(self, gravity, ground_y):
        pass

    def jump(self):
        pass

    def attack(enemies):
        pass

    def get_rect(self):
        return self.rect

    def get_img(self):
        return self.img