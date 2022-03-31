from Tank1990.resources.entity.Player import Player
class Team:

    def __init__(self, name: str):
        self.name = name
        self.players = []

    def getPlayers(self):
        return self.players

    def addPlayer(self, player: Player):
        self.players.append(Player)

    def clearPlayers(self):
        self.players.clear()
    
    def removePlayer(self, player: Player):
        self.players.remove(player)

