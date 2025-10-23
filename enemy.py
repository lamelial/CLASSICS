import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def draw(self, surface): # inherit a class ?
        surface.blit(self.img, self.rect)