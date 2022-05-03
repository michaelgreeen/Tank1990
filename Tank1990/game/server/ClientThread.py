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
    player.color_string = color
    print("PLAYER LIST:\n")
    for player_object in server.teams.get("Red").getPlayers() + server.teams.get("Green").getPlayers():
        print(str(player_object.x) + " " + str(player_object.y) + " " + player_object.color_string + "\n")
    if color == "RED":
        player.color = RED
    else:
        player.color = GREEN

    while True:
        try:
            reply = ""
            data = connection.recv(2048//2).decode()


            if not data:
                print("Disconnected")
                break

            else:
                player_info = read_pos_team(data)
                player.x = player_info[0]
                player.y = player_info[1]
                player.color = player_info[2]
                player_list = server.teams.get("Red").getPlayers() + server.teams.get("Green").getPlayers()
                for player_object in player_list:
                    reply += str(player_object.x) + "," + str(player_object.y) + "," + player_object.color_string + "\n"
                connection.sendall(str.encode(reply))

            print("Received: ", data)
            print("Sending : ", reply)
            
        except:
            break

    PLAYER_TEAMS_LOCK.acquire()
    print("REMOVING: " + str(player.x) + "," + str(player.y) + "," + player.color_string + "\n")
    server.removePlayer(player)
    PLAYER_TEAMS_LOCK.release()
    print("Lost connection")
    print("CURRENT PLAYER LIST: \n")
    for player_object in server.teams.get("Red").getPlayers() + server.teams.get("Green").getPlayers():
        print(str(player_object.x) + " " + str(player_object.y) + " " + player_object.color_string + "\n")
    connection.close()