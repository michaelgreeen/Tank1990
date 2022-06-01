import pickle
from socket import socket

from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Player.PlayerSlot import PlayerSlot
from Tank1990.resources.entity.Tank.Tank import Tank
from Tank1990.resources.message_types.bulletCreateMessage.BulletCreateMessage import BulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.BulletUpdateRequest import BulletUpdateRequest
from Tank1990.resources.message_types.mapUpdateMessage.MapUpdateMessage import MapUpdateMessage
from Tank1990.resources.message_types.playerCreateMessage.PlayerCreateMessage import PlayerCreateMessage
from Tank1990.resources.message_types.tankUpdateMessage.BatchTankUpdateMessage import BatchTankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateMessage import TankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateRequest import TankUpdateRequest

def botControl(server, bot_player):
    pass
def botThread(server):
    while True:
        for player_slot in server.player_slots:
            if server.player_slots[player_slot].isBot:
                botControl(server, server.player_slots[player_slot].player)
                pass
            else:
                continue




