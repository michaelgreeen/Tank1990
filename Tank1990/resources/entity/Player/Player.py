import pickle

from Tank1990.resources.configuration.Common import CLIENT_STARTING_POSITIONS, CLIENT_STARTING_DIRECTION_VECTOR
from Tank1990.resources.entity.Tank.Tank import Tank
from Tank1990.resources.entity.Team.Team import Team


class Player():
    def __init__(self, id):
        self.id = id

    def assignTank(self, tank: Tank):
        self.tank = tank

    def assignToTeam(self, team: Team):
        self.team = team
        team.addPlayer(self)

    def respawnTank(self):
        self.tank.x, self.tank.y = CLIENT_STARTING_POSITIONS[self.id]
        self.tank.direction_vector = CLIENT_STARTING_DIRECTION_VECTOR[self.id]



