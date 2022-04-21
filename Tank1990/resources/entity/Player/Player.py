import pickle


from Tank1990.resources.entity.Tank.Tank import Tank
from Tank1990.resources.entity.Team.Team import Team


class Player():
    def __init__(self, id):
        self.id = id
        self.tank: Tank
        self.team: Team

    def assignTank(self, tank: Tank):
        self.tank = tank

    def assignToTeam(self, team: Team):
        self.team = team
        team.addPlayer(self)

    def serializePlayer(self):
        return pickle.dumps(self)
