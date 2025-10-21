import pygame
import sys
from player import Player
from camera import Camera

class Game:
    WIDTH, HEIGHT = 800, 400
    CLAY = (166, 92, 50)
    BLACK = (26, 26, 26)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("GRS383")
        self.clock = pygame.time.Clock()
        self.running = True

        self.meander_img = pygame.image.load("assets/key.png").convert_alpha()
        self.meander_img = pygame.transform.scale_by(self.meander_img, 0.5)

        self.player = Player(100, self.HEIGHT - 200)
        self.camera = Camera(self.WIDTH, self.HEIGHT)

        # physics
        self.gravity = 0.8
        self.ground_y = self.HEIGHT - 50

    def draw_meander_image(self, surface, image, offset, y):
        img_width = image.get_width()
        start_x = int(offset) % img_width
        for x in range(-img_width, self.WIDTH + img_width, img_width):
            surface.blit(image, (x - start_x, y))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            pygame.transform.flip(self.player.get_img(), True, False)
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_SPACE]:
            self.player.jump()
        self.player.move(dx)

    def update(self):
        self.player.update(self.gravity, self.ground_y)
        self.camera.follow(self.player.get_rect(), self.WIDTH)

    def draw(self):
        self.screen.fill(self.CLAY)
        pygame.draw.rect(self.screen, self.BLACK, (0, self.ground_y, self.WIDTH, 50))

        self.draw_meander_image(self.screen, self.meander_img, self.camera.offset_x * 0.5, 10)
        self.draw_meander_image(self.screen, self.meander_img, self.camera.offset_x * 0.5, self.HEIGHT - 10 )

        player_rect_cam = self.camera.apply(self.player.get_rect())
        self.screen.blit(self.player.get_img(), player_rect_cam)

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
