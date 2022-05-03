import pygame
from Tank1990.resources.configuration.Common import *

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
        self.rows = len(self.MapObjects)
        self.columns = len(self.MapObjects[0])
        self.brick = pygame.transform.scale(pygame.image.load(r"C:\Users\mifas\OneDrive\Pulpit\projectDistributedProcessing-main\projectDistributedProcessing\Tank1990\app\game\img\brick.png"),(SCREEN_WIDTH/self.columns,SCREEN_HEIGHT/self.rows))
        self.road = pygame.transform.scale(pygame.image.load(r"C:\Users\mifas\OneDrive\Pulpit\projectDistributedProcessing-main\projectDistributedProcessing\Tank1990\app\game\img\road.png"),(SCREEN_WIDTH/self.columns,SCREEN_HEIGHT/self.rows))
        self.sand = pygame.transform.scale(pygame.image.load(r"C:\Users\mifas\OneDrive\Pulpit\projectDistributedProcessing-main\projectDistributedProcessing\Tank1990\app\game\img\sandbagBeige.png"),(SCREEN_WIDTH/self.columns,SCREEN_HEIGHT/self.rows))

    def changeMapState(self, coordinate: tuple, objectType: int):
        self.MapObjects[coordinate[0]][coordinate[1]] = objectType

    def draw(self, win):

        intervalHorizontal = SCREEN_WIDTH / self.columns
        intervalVertical = SCREEN_HEIGHT / self.rows
        for i in range(self.rows):
            for j in range(self.columns):
                if self.MapObjects[i][j] == 0:
                    win.blit(self.road,(intervalVertical * j, intervalHorizontal * i))
                elif self.MapObjects[i][j] == 1:
                    win.blit(self.brick,(intervalVertical * j, intervalHorizontal * i))
                elif self.MapObjects[i][j] == 2:
                    win.blit(self.sand,(intervalVertical * j, intervalHorizontal * i))
