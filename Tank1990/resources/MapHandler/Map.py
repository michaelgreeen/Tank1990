import pygame
from Tank1990.resources.configuration.Common import *


BLUE = (65,105,225)
GREEN = (48,128,20)
BLACK = (0,0,0)
BRICK = (255,55,50)

class Map:
    def __init__(self):
        self.MapObjects = [[0, 2, 2, 1, 2, 1, 2, 1, 2, 1],
                           [0, 0, 2, 0, 0, 0, 0, 2, 2, 1],
                           [0, 0, 2, 2, 0, 0, 2, 2, 2, 1],
                           [0, 0, 2, 2, 0, 1, 2, 2, 2, 1],
                           [1, 1, 1, 1, 1, 2, 2, 2, 2, 1],
                           [1, 0, 2, 1, 1, 1, 2, 2, 2, 1],
                           [2, 0, 0, 2, 0, 1, 2, 2, 2, 1],
                           [2, 0, 1, 1, 1, 1, 1, 2, 2, 1],
                           [2, 0, 1, 2, 0, 1, 1, 2, 2, 1],
                           [2, 0, 1, 2, 0, 1, 1, 2, 2, 1],
                           ]

    def changeMapState(self, coordinate: tuple, objectType: int):
        self.MapObjects[coordinate[0]][coordinate[1]] = objectType

    def draw(self, win):
        rows = len(self.MapObjects)
        columns = len(self.MapObjects[0])
        intervalVertical = SCREEN_WIDTH / columns
        intervalHorizontal = SCREEN_HEIGHT / rows
        for i in range(rows):
            for j in range(columns):
                if self.MapObjects[i][j] == 0:
                    pygame.draw.rect(win, BLACK,
                                     (intervalHorizontal * j, intervalVertical * i, intervalHorizontal,
                                      intervalVertical))
                elif self.MapObjects[i][j] == 1:
                    pygame.draw.rect(win, BRICK,
                                     (intervalHorizontal * j, intervalVertical * i, intervalHorizontal,
                                      intervalVertical))
                elif self.MapObjects[i][j] == 2:
                    pygame.draw.rect(win, GREEN,
                                     (intervalHorizontal * j, intervalVertical * i, intervalHorizontal,
                                      intervalVertical))
