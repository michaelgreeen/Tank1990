import pickle
from socket import socket

from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Player.PlayerSlot import PlayerSlot
from Tank1990.resources.entity.Tank.Tank import Tank
from Tank1990.resources.message_types.bulletCreateMessage.bulletCreateMessage import bulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.bulletUpdateRequest import bulletUpdateRequest
from Tank1990.resources.message_types.mapUpdateMessage.mapUpdateMessage import mapUpdateMessage
from Tank1990.resources.message_types.playerCreateMessage.playerCreateMessage import playerCreateMessage
from Tank1990.resources.message_types.tankUpdateMessage.batchTankUpdateMessage import batchTankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateMessage import tankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateRequest import tankUpdateRequest

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




