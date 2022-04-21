import pickle
from socket import socket



from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Tank.Tank import Tank
from Tank1990.resources.message_types.bulletCreateMessage.bulletCreateMessage import bulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.bulletUpdateRequest import bulletUpdateRequest
from Tank1990.resources.message_types.playerCreateMessage.playerCreateMessage import playerCreateMessage
from Tank1990.resources.message_types.tankUpdateMessage.batchTankUpdateMessage import batchTankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateMessage import tankUpdateMessage

def clientThread(server, connection: socket, playerNumber: int):
    

    spawnPoint = CLIENT_STARTING_POSITIONS[playerNumber]
    initialDirectionVector = CLIENT_STARTING_DIRECTION_VECTOR[playerNumber]
    player: Player = Player(playerNumber)
    server.addPlayer(player)
    playerTank: Tank = Tank(spawnPoint[0], spawnPoint[1],  initialDirectionVector, player.team.color)
    player.assignTank(playerTank)
    initPlayerMessage = playerCreateMessage(player)
    print("SENDING: ", initPlayerMessage)
    connection.send(initPlayerMessage.getMessage())
    print("PLAYER LIST:\n")
    for player_object in server.teams.get("Red").players + server.teams.get("Green").players:
        print(str(player_object.tank.x) + " " + str(player_object.tank.y) + " " + player_object.team.name + "\n")


    while True:
        try:
            
            data = pickle.loads(connection.recv(4096//1))
            if not data:
                print("Disconnected")
                break
            elif isinstance(data, tankUpdateMessage):
                reply = batchTankUpdateMessage()
                tankUpdate: tankUpdateMessage = data
                player.tank.x = tankUpdate.new_x
                player.tank.y = tankUpdate.new_y
                player.tank.direction_vector = tankUpdate.new_direction_vector
                player_list = server.teams.get("Red").players + server.teams.get("Green").players
                for player_object in player_list:
                    reply.addTankUpdateMessage(tankUpdateMessage(player_object.id, player_object.tank.x, player_object.tank.y, player_object.tank.direction_vector, player_object.team.color))
                connection.sendall(reply.getMessage())

            elif isinstance(data, bulletCreateMessage):
                sent_to_player_flags = [False, False, False, False]
                server.bullet_objects_queue.append((data.bullet, sent_to_player_flags))
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, bulletUpdateRequest):
                reply = data
                bullet_objects_to_send = []
                for bullet_object_to_create in server.bullet_objects_queue:
                    if not bullet_object_to_create[1][playerNumber]:
                        bullet_objects_to_send.append(bullet_object_to_create[0])
                        bullet_object_to_create[1][playerNumber] = True
                for bullet in bullet_objects_to_send:
                    reply.bullets_to_add.append(bulletCreateMessage(bullet))
                connection.sendall(reply.getMessage())
                for bullet_object_to_create in server.bullet_objects_queue:
                    to_delete = False
                    for flag_index in range(len(server.teams.get("Red").players + server.teams.get("Green").players)):
                        if bullet_object_to_create[1][flag_index]:
                            pass
                        else:
                            to_delete = False
                    if to_delete:
                        server.bullet_objects_queue.remove(bullet_object_to_create)


            else:
                pass

            print("Received: ", data)
            print("Sending : ", reply)
            
        except:
            break


    print("REMOVING: " + str(player.tank.x) + "," + str(player.tank.y) + "," + player.team.name + "\n")
    server.removePlayer(player)

    print("Lost connection")
    print("CURRENT PLAYER LIST: \n")
    for player_object in server.teams.get("Red").players + server.teams.get("Green").players:
        print(str(player_object.tank.x) + " " + str(player_object.tank.y) + " " + player_object.team.name + "\n")
    connection.close()