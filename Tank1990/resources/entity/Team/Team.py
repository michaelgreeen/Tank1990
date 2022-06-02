class Team:

    def __init__(self, name: str, color: tuple):
        self.name = name
        self.color = color
        self.order_issuing_player = None
        self.players = []


    def addPlayer(self, player):
        self.players.append(player)

    def clearPlayers(self):
        self.players.clear()

    def removePlayer(self, player):
        self.players.remove(player)
