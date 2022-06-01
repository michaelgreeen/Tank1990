import pickle

from Tank1990.resources.entity.Player.Player import Player


class PlayerCreateMessage:
    def __init__(self, player: Player, mapOutline):
        self.player = player
        self.mapOutline = mapOutline


    def getMessage(self):
        return pickle.dumps(self)
