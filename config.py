import pygame

# dimensions
WIDTH, HEIGHT = 800, 400

# colours
CLAY = (166, 92, 50)
BLACK = (10, 10, 10)
SAND = (220, 190, 120)
RED = (180, 40, 40)
WHITE = (245, 245, 245)

# physics
GRAVITY = 0.8
GROUND_Y = HEIGHT - 60

def tint_surface(surface, tint_color):
    """Multiply each pixel by tint_color."""
    tinted = surface.copy()
    tint = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    tint.fill(tint_color)
    tinted.blit(tint, (0, 0), special_flags=pygame.BLEND_MULT)
    return tinted