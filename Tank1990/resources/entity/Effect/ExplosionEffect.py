import pygame

from Tank1990.resources.configuration.Common import SMOKE_WIDTH, SMOKE_HEIGHT


class ExplosionEffect:
    def __init__(self, x, y):
        self.stage_counter = 0
        self.x = x
        self.y = y
        self.stage_img = []
        for i in range(5):
            self.stage_img += pygame.transform.scale(pygame.image.load("..\\img\\" + "Smoke" + i + ".png"),
                                                     (SMOKE_WIDTH, SMOKE_HEIGHT))
            
    def update(self):
        self.stage_counter += 1

    def draw(self, win):
        win.blit(self.stage_img[self.stage_counter], (self.x, self.y))