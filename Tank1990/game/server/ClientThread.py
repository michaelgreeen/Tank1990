import threading
from socket import socket
from tkinter import colorchooser
from Tank1990.game.server.Server import PLAYER_TEAMS_LOCK
from Tank1990.resources.entity.Player.Player import Player
from Tank1990.conf.Common import *
from Tank1990.game.server.Server import Server

def clientThread(server: Server, connection: socket, playerNumber: int):
    connection.send(str.encode(make_pos_team((CLIENT_STARTING_POSITIONS[playerNumber][0], CLIENT_STARTING_POSITIONS[playerNumber][1], "RED"))))
    
    player: Player = Player(CLIENT_STARTING_POSITIONS[playerNumber][0], CLIENT_STARTING_POSITIONS[playerNumber][1], VEHICLE_WIDTH, VEHICLE_HEIGHT, "") 
    PLAYER_TEAMS_LOCK.acquire()
    color: str = server.addPlayer(player)
    PLAYER_TEAMS_LOCK.release()
    if color == "RED":
        player.color = RED
    else:
        player.color = GREEN
    reply = ""
    while True:
        try:
            data = read_pos_team(connection.recv(2048/2).decode())
            player.x = data[0]
            player.y = data[1]
            player.color = data[2]

            if not data:
                print("Disconnected")
                break
            else:
                reply = (player.x, player.y, [color])

                print("Received: ", data)
                print("Sending : ", reply)

            connection.sendall(str.encode(make_pos_team(reply)))
        except:
            break
    PLAYER_TEAMS_LOCK.acquire()
    server.removePlayer(player)
    PLAYER_TEAMS_LOCK.release()
    print("Lost connection")
    connection.close()