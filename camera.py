class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.width = width
        self.height = height

    def follow(self, target_rect, screen_width):
        self.offset_x = target_rect.centerx - screen_width // 6

    def apply(self, rect):
        return rect.move(-self.offset_x, 0)
