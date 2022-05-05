import pickle

from Tank1990.resources.entity.Player.Player import Player


class playerCreateMessage:
    def __init__(self, player, mapOutline):
        self.player = player
        self.mapOutline = mapOutline

    def getMessage(self):
        return pickle.dumps(self)
