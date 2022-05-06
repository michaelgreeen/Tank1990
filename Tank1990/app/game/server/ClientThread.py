import pickle
from socket import socket



from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Tank.Tank import Tank
from Tank1990.resources.message_types.bulletCreateMessage.bulletCreateMessage import bulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.bulletUpdateRequest import bulletUpdateRequest
from Tank1990.resources.message_types.mapUpdateMessage.mapUpdateMessage import mapUpdateMessage
from Tank1990.resources.message_types.playerCreateMessage.playerCreateMessage import playerCreateMessage
from Tank1990.resources.message_types.tankUpdateMessage.batchTankUpdateMessage import batchTankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateMessage import tankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateRequest import tankUpdateRequest


def clientThread(server, connection: socket):
    player_number = 0
    for slot in server.player_slots:
        if server.player_slots[slot] is None:
            player_number = slot
            break
        else:
            pass

    spawnPoint = CLIENT_STARTING_POSITIONS[player_number]
    initialDirectionVector = CLIENT_STARTING_DIRECTION_VECTOR[player_number]
    player = Player(player_number)
    server.addPlayer(player)
    player_tank = Tank(spawnPoint[0], spawnPoint[1],  initialDirectionVector, player.team.color)
    player.assignTank(player_tank)
    server.player_slots[player_number] = player
    initPlayerMessage = playerCreateMessage(player,server.mapOutline)

    #print("SENDING: ", initPlayerMessage)
    connection.send(initPlayerMessage.getMessage())
    #print("PLAYER LIST:\n")
    #for player_object in server.teams.get("Red").players + server.teams.get("Green").players:
    #    print(str(player_object.tank.x) + " " + str(player_object.tank.y) + " " + player_object.team.name + "\n")


    while True:
        try:
            
            data = pickle.loads(connection.recv(4096//1))
            if not data:
                print("Disconnected")
                break

            elif isinstance(data, tankUpdateMessage):
                server.message_queues_lock.get("PLAYER_MOVE_LOCK").acquire()
                server.message_queues.get("PLAYER_MOVE").append((player_number, data.direction_vector))
                server.message_queues_lock.get("PLAYER_MOVE_LOCK").release()
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, bulletCreateMessage):
                server.message_queues_lock.get("BULLET_CREATE_LOCK").acquire()
                server.message_queues.get("BULLET_CREATE").append(player_number)
                server.message_queues_lock.get("BULLET_CREATE_LOCK").release()
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, tankUpdateRequest):
                for player in server.teams.get("Red").players + server.teams.get("Green").players:
                    tank = player.tank
                    if tank is not None:
                        data.tanks.append(player.tank)
                reply = data
                connection.sendall(reply.getMessage())
            elif isinstance(data, bulletUpdateRequest):
                for bullet in server.bullet_objects:
                    data.bullets.append(bullet)
                reply = data
                connection.sendall(reply.getMessage())
            elif isinstance(data, mapUpdateMessage):
                data.map_outline = server.mapOutline
                reply = data
                connection.sendall(reply.getMessage())
            else:
                pass

            #print("Received: ", data)
            #print("Sending : ", reply)
            
        except:
            break


    #print("REMOVING: " + str(player.tank.x) + "," + str(player.tank.y) + "," + player.team.name + "\n")
    server.removePlayer(player)

    #print("Lost connection")
    #print("CURRENT PLAYER LIST: \n")
    #for player_object in server.teams.get("Red").players + server.teams.get("Green").players:
    #    print(str(player_object.tank.x) + " " + str(player_object.tank.y) + " " + player_object.team.name + "\n")
    connection.close()