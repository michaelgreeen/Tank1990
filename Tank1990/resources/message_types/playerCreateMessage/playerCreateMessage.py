import pickle

from Tank1990.resources.entity.Player.Player import Player


class playerCreateMessage:
    def __init__(self, player: Player):
        self.player = player


    def getMessage(self):
        return pickle.dumps(self)
