from abc import abstractmethod, ABC
from Tank1990.resources.configuration.Common import *


class MapElement(ABC):
    def __init__(self, x, y, path):
        self.x = INTERVAL_HORIZONTAL * x
        self.y = INTERVAL_VERTICAL * y
        self.width = INTERVAL_HORIZONTAL
        self.height = INTERVAL_VERTICAL
        self.body_img_path = path

    @abstractmethod
    def collision(self):
        pass
