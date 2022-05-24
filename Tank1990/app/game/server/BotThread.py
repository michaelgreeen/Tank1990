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


def botThread(server):
    bot_number = 0
    for slot in server.player_slots:
        if server.player_slots[slot] is None:
            bot_number = slot
            break
        else:
            continue
    bot_player = Player(bot_number)
    spawnPoint = CLIENT_STARTING_POSITIONS[bot_number]
    initialDirectionVector = CLIENT_STARTING_DIRECTION_VECTOR[bot_number]
    server.addPlayer(bot_player)
    player_tank = Tank(spawnPoint[0], spawnPoint[1], initialDirectionVector, bot_player.team.color)
    bot_player.assignTank(player_tank)
    server.player_slots[bot_number] = PlayerSlot(bot_player, True)
    while(True):
        if server.thread_list[bot_number][1]:
            return
        pass




