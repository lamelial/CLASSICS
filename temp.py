import pygame
import sys
import player

pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GRS383")

CLAY = (166, 92, 50)
BLACK = (26, 26, 26)
LIGHT_CLAY = (212, 140, 82)

clock = pygame.time.Clock()

meander_img = pygame.image.load("key.png").convert_alpha()
scale_factor = 0.5
meander_img = pygame.transform.scale_by(meander_img, scale_factor)



player_vel_y = 0
on_ground = True
scroll_x = 0
speed = 5
gravity = 0.8
jump_strength = -15

layer_speeds = [0.3, 0.6, 1.0]

def draw_meander_image(surface, image, offset, y):
    """Draws a repeating meander image horizontally across the screen."""
    img_width = image.get_width()
    # normalize offset so it wraps cleanly
    x_offset = int(offset) % img_width
    for x in range(-img_width, WIDTH + img_width, img_width):
        surface.blit(image, (x + x_offset, y))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        scroll_x += speed
    if keys[pygame.K_RIGHT]:
        scroll_x -= speed
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = jump_strength
        on_ground = False

    player_vel_y += gravity
    player_rect.y += player_vel_y

    if player_rect.bottom >= HEIGHT - 50:
        player_rect.bottom = HEIGHT - 50
        player_vel_y = 0
        on_ground = True

    # --- DRAW ---
    screen.fill(CLAY)

    # Background Greek temple silhouettes (slow)
    for x in range(-2000, 2000, 300):
        pygame.draw.polygon(screen, BLACK,
                            [(x + scroll_x * layer_speeds[0], HEIGHT - 150),
                             (x + 150 + scroll_x * layer_speeds[0], 180),
                             (x + 300 + scroll_x * layer_speeds[0], HEIGHT - 150)])

    # Ground strip (fast)
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 50, WIDTH, 50))
    # Player silhouette
    screen.blit(player_img, player_rect)

    draw_meander_image(screen, meander_img, scroll_x * 0.5, 10)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
