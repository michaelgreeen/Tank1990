from abc import abstractmethod, ABC
import pygame
from Tank1990.resources.configuration.Common import SCREEN_WIDTH, SCREEN_HEIGHT

columns = 10
rows = 10
intervalVertical = SCREEN_WIDTH / columns
intervalHorizontal = SCREEN_HEIGHT / rows


class MapElement(ABC):
    def __init__(self, x, y, path):
        self.x = intervalHorizontal * x
        self.y = intervalVertical * y
        self.width = intervalHorizontal
        self.height = intervalVertical
        self.body_img_path = path

    @abstractmethod
    def collision(self):
        pass
