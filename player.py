import pygame

class Player:
    _PLAYER_VEL



player_img = pygame.image.load("achilles.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (80 * 1.5, 120 * 1.5))

# Create a rect for position and collision
player_rect = player_img.get_rect()
player_rect.x = 100
player_rect.y = HEIGHT - 100