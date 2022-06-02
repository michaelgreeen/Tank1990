import pickle

from Tank1990.resources.message_types.bulletCreateMessage.BulletCreateMessage import BulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.BulletUpdateRequest import BulletUpdateRequest
from Tank1990.resources.message_types.crowdControlMessage.RequestOrderIssuance import RequestOrderIssuance
from Tank1990.resources.message_types.crowdControlMessage.CreateCrowdFollowMessage import CreateCrowdFollowMessage
from Tank1990.resources.message_types.crowdControlMessage.TargetGridMessage import TargetGridMessage
from Tank1990.resources.message_types.mapUpdateMessage.MapUpdateMessage import MapUpdateMessage
from Tank1990.resources.message_types.playerCreateMessage.PlayerCreateMessage import PlayerCreateMessage
from Tank1990.resources.message_types.requestMapEvents.RequestMapEvents import RequestMapEvents
from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateMessage import TankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateRequest import TankUpdateRequest


def clientThread(server, connection, player_number):

    player = server.player_slots[player_number].player
    server.player_slots[player_number].isBot = False
    initPlayerMessage = PlayerCreateMessage(player, server.mapOutline)
    connection.send(initPlayerMessage.getMessage())

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
                for player_entry in server.teams.get("Red").players + server.teams.get("Green").players:
                    tank = player_entry.tank
                    if tank is not None:
                        data.tanks.append(player_entry.tank)
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
                server.player_map_events_locks[player_number].acquire()
                for map_event in server.player_map_events[player_number]:
                    data.map_event_list.append(map_event)
                server.player_map_events[player_number].clear()
                server.player_map_events_locks[player_number].release()
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, CreateCrowdFollowMessage):
                server.message_queues_lock.get("FOLLOW_EVENT_LOCK").acquire()
                server.message_queues.get("FOLLOW_EVENT").append((data.tank, data.followRequest))
                server.message_queues_lock.get("FOLLOW_EVENT_LOCK").release()
                data.tank = server.player_slots[player_number].player.tank
                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, RequestOrderIssuance):
                if data.issuing_player_id is None:
                    if player.team.order_issuing_player is not None:
                        data.issuing_player_id = player.team.order_issuing_player.id
                else:
                    player.team.order_issuing_player = player
                    data.issuing_player_id = player_number

                reply = data
                connection.sendall(reply.getMessage())

            elif isinstance(data, TargetGridMessage):
                if player.team.order_issuing_player == player:
                    player.team.target_grid = data.target_grid
                data.target_grid = player.team.target_grid
                reply = data
                connection.sendall(reply.getMessage())

            else:
                pass
            
        except:
            break

    server.player_slots[player_number].isBot = True
    connection.close()