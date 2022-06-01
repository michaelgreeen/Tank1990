import pickle

from Tank1990.resources.message_types.bulletCreateMessage.BulletCreateMessage import BulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.BulletUpdateRequest import BulletUpdateRequest
from Tank1990.resources.message_types.crowdControlMessage.CreateCrowdFollowMessage import CreateCrowdFollowMessage
from Tank1990.resources.message_types.mapUpdateMessage.MapUpdateMessage import MapUpdateMessage
from Tank1990.resources.message_types.playerCreateMessage.PlayerCreateMessage import PlayerCreateMessage
from Tank1990.resources.message_types.requestMapEvents.RequestMapEvents import RequestMapEvents
from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateMessage import TankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateRequest import TankUpdateRequest


def clientThread(server, connection, player_number):

    player = server.player_slots[player_number].player
    server.player_slots[player_number].isBot = False
    #spawnPoint = CLIENT_STARTING_POSITIONS[player_number]
    #initialDirectionVector = CLIENT_STARTING_DIRECTION_VECTOR[player_number]
    #player = Player(player_number)
    #server.addPlayer(player)
    #player_tank = Tank(spawnPoint[0], spawnPoint[1],  initialDirectionVector, player.team.color)
    #player.assignTank(player_tank)
    #server.player_slots[player_number] = player
    initPlayerMessage = PlayerCreateMessage(player, server.mapOutline)

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

            elif isinstance(data, TankUpdateMessage):
                server.message_queues_lock.get("PLAYER_MOVE_LOCK").acquire()
                server.message_queues.get("PLAYER_MOVE").append((player_number, data.direction_vector))
                server.message_queues_lock.get("PLAYER_MOVE_LOCK").release()
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, BulletCreateMessage):
                server.message_queues_lock.get("BULLET_CREATE_LOCK").acquire()
                server.message_queues.get("BULLET_CREATE").append(player_number)
                server.message_queues_lock.get("BULLET_CREATE_LOCK").release()
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, TankUpdateRequest):
                for player in server.teams.get("Red").players + server.teams.get("Green").players:
                    tank = player.tank
                    if tank is not None:
                        data.tanks.append(player.tank)
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, BulletUpdateRequest):
                for bullet in server.bullet_objects:
                    data.bullets.append(bullet)
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, MapUpdateMessage):
                data.map_outline = server.mapOutline
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, RequestMapEvents):
                server.message_queues_lock.get("MAP_EVENT_LOCK").acquire()

                for map_event in server.message_queues.get("MAP_EVENT"):
                    if not map_event[1][player_number]:
                        data.map_event_list.append(map_event[0])
                    map_event[1][player_number] = True
                    toDelete = False
                    for sentToPlayer in map_event[1]:
                        toDelete = toDelete and sentToPlayer
                    if toDelete:
                        server.message_queue.get("MAP_EVENT").remove(map_event)

                server.message_queues_lock.get("MAP_EVENT_LOCK").release()

                reply = data
                print(reply.getMessage())
                connection.sendall(reply.getMessage())

            elif isinstance(data, CreateCrowdFollowMessage):
                server.message_queues_lock.get("FOLLOW_EVENT_LOCK").acquire()
                server.message_queues.get("FOLLOW_EVENT").append((data.tank,data.followRequest))
                server.message_queues_lock.get("FOLLOW_EVENT_LOCK").release()
                data.tank = server.player_slots[player_number].player.tank
                reply = data
                connection.sendall(reply.getMessage())
            else:
                pass
            
        except:
            break


    #print("REMOVING: " + str(player.tank.x) + "," + str(player.tank.y) + "," + player.team.name + "\n")
    server.removePlayer(player)

    #print("Lost connection")
    #print("CURRENT PLAYER LIST: \n")
    #for player_object in server.teams.get("Red").players + server.teams.get("Green").players:
    #    print(str(player_object.tank.x) + " " + str(player_object.tank.y) + " " + player_object.team.name + "\n")
    connection.close()