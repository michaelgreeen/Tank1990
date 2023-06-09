import pygame

from Tank1990.resources.configuration.Common import SMOKE_WIDTH, SMOKE_HEIGHT, INTERVAL_VERTICAL, INTERVAL_HORIZONTAL


class ExplosionEffect:
    def __init__(self, x, y):
        self.stage_counter = 0
        self.x = x
        self.y = y
        self.stage_img = ["..\\img\\Smoke0.png", "..\\img\\Smoke1.png", "..\\img\\Smoke2.png",
                          "..\\img\\Smoke3.png", "..\\img\\Smoke4.png"]
        self.center = (x - INTERVAL_HORIZONTAL/2, y - INTERVAL_VERTICAL/2)

    def update(self):
        self.stage_counter += 0.2

    def draw(self, win):
        image = pygame.image.load(self.stage_img[int(self.stage_counter)])
        image = pygame.transform.scale((image), (SMOKE_WIDTH, SMOKE_HEIGHT))
        win.blit(image, self.center)