import pygame
import config
from enemy import Enemy
from gate import Gate


class Player(pygame.sprite.Sprite):
    _SPEED = 5
    _IMG_PATH = "assets/achilles2.png"
    _JUMP_STRENGTH = -15

    def __init__(self, x, y):
        super().__init__()
        self.forward_img = pygame.transform.scale(pygame.image.load(self._IMG_PATH).convert_alpha(), (int(512 * 0.4), int(587 * 0.4)))
        self.backward_img = pygame.transform.flip(self.forward_img, True, False)
        self.img = self.forward_img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = True
        self.facing_right = True
        self.attack_cooldown = 400
        self.last_attack_time = 0
        self.attack_range = 50

        self.spoils = 0

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

    def update(self):
        self.vel_y += config.GRAVITY
        self.rect.y += self.vel_y

        # ground collision
        if self.rect.bottom >= config.GROUND_Y:
            self.rect.bottom = config.GROUND_Y
            self.vel_y = 0
            self.on_ground = True

    def get_rect(self):
        return self.rect

    def get_img(self):
        return self.img

    def add_spoils(self, amount):
        self.spoils += amount

    def attack(self, enemies, objects):
        now = pygame.time.get_ticks()

        if now - self.last_attack_time < self.attack_cooldown:
            return

        self.last_attack_time = now

        player_rect = self.rect
        facing_right = self.facing_right
        attack_width = 50

        if facing_right:
            attack_rect = pygame.Rect(
                player_rect.right,
                player_rect.y,
                attack_width,
                player_rect.height
            )
        else:
            attack_rect = pygame.Rect(
                player_rect.left - attack_width,
                player_rect.y,
                attack_width,
                player_rect.height
            )

        # hit enemies
        for enemy in enemies:
            if attack_rect.colliderect(enemy.rect):
                enemy.take_damage(self)
        for ob in objects:
            if ob.solid and attack_rect.colliderect(ob.rect):
                ob.take_damage()
