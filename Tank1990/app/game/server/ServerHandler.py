import pygame
import random
from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import SCREEN_WIDTH, SCREEN_HEIGHT, DOWN_UNIT_VECTOR, UP_UNIT_VECTOR, \
    RIGHT_UNIT_VECTOR, LEFT_UNIT_VECTOR, VEHICLE_WIDTH, VEHICLE_HEIGHT, INTERVAL_HORIZONTAL, INTERVAL_VERTICAL, \
    VEHICLE_VELOCITY, MAP_ROWS, MAP_COLUMNS, CLIENT_STARTING_DIRECTION_VECTOR, CLIENT_STARTING_POSITIONS, PLAYER_COUNT
from Tank1990.resources.entity.Player.PlayerSlot import PlayerSlot
from Tank1990.resources.entity.Tank.Tank import Tank


def createBots(server):
    for bot_number in range(PLAYER_COUNT):
        bot_player = Player(bot_number)
        spawnPoint = CLIENT_STARTING_POSITIONS[bot_number]
        initialDirectionVector = CLIENT_STARTING_DIRECTION_VECTOR[bot_number]
        server.addPlayer(bot_player)
        player_tank = Tank(spawnPoint[0], spawnPoint[1], initialDirectionVector, bot_player.team.color)
        bot_player.assignTank(player_tank)
        server.player_slots[bot_number] = PlayerSlot(bot_player, True)


def handleBots(server):
    for bot_number in range(PLAYER_COUNT):
        if server.player_slots[bot_number].isBot:
            server.message_queues_lock.get("PLAYER_MOVE_LOCK").acquire()
            server.message_queues.get("PLAYER_MOVE").append((bot_number, random.choice(CLIENT_STARTING_DIRECTION_VECTOR)))
            server.message_queues_lock.get("PLAYER_MOVE_LOCK").release()
            if random.randint(0, 100) < 50:
                server.message_queues_lock.get("BULLET_CREATE_LOCK").acquire()
                server.message_queues.get("BULLET_CREATE").append(bot_number)
                server.message_queues_lock.get("BULLET_CREATE_LOCK").release()

    pass

def updateTanks(server):
    server.message_queues_lock.get("PLAYER_MOVE_LOCK").acquire()
    for player_id, direction_vector in server.message_queues.get("PLAYER_MOVE"):
        player_tank = server.player_slots.get(player_id).player.tank
        if player_tank is not None:
            # if checkMovingCollision(player_tank,server.mapOutline):
            player_tank.move(direction_vector, server.mapOutline)
    for player in (server.teams.get("Green").players + server.teams.get("Red").players):
        player_tank = player.tank
        if player_tank is not None:
            player.tank.update()

    server.message_queues.get("PLAYER_MOVE").clear()
    server.message_queues_lock.get("PLAYER_MOVE_LOCK").release()


def createBullets(server):
    server.message_queues_lock.get("BULLET_CREATE_LOCK").acquire()
    for player_id in server.message_queues.get("BULLET_CREATE"):
        player_tank = server.player_slots[player_id].player.tank
        bullet = player_tank.shoot()
        if bullet is not None:
            server.bullet_objects.append(bullet)
    server.message_queues.get("BULLET_CREATE").clear()
    server.message_queues_lock.get("BULLET_CREATE_LOCK").release()


def updateBullets(server):
    for bullet in server.bullet_objects:
        bullet.update()


def bulletCollisionCheck(server):
    for bullet in server.bullet_objects:
        bullet_x_grid = int(bullet.x // INTERVAL_HORIZONTAL)
        bullet_y_grid = int(bullet.y // INTERVAL_VERTICAL)
        if bullet.x > SCREEN_WIDTH or bullet.x < 0:
            server.bullet_objects.remove(bullet)
            continue
        if bullet.y > SCREEN_HEIGHT or bullet.y < 0:
            server.bullet_objects.remove(bullet)
            continue
        if server.mapOutline[bullet_y_grid][bullet_x_grid] == 1 or server.mapOutline[bullet_y_grid][bullet_x_grid] == 3:
            server.mapOutline[bullet_y_grid][bullet_x_grid] = 2

            server.bullet_objects.remove(bullet)
            continue

        for player in (server.teams.get("Green").players + server.teams.get("Red").players):
            tank = player.tank
            if tank is not None:
                if bullet.color != player.team.color:
                    if tank.direction_vector == RIGHT_UNIT_VECTOR or tank.direction_vector == LEFT_UNIT_VECTOR:
                        left_tank_boundary = tank.center[0] - VEHICLE_WIDTH / 2
                        right_tank_boundary = tank.center[0] + VEHICLE_WIDTH / 2
                        upper_tank_boundary = tank.center[1] - VEHICLE_HEIGHT / 2
                        down_tank_boundary = tank.center[1] + VEHICLE_HEIGHT / 2
                        if left_tank_boundary < bullet.x < right_tank_boundary and upper_tank_boundary < bullet.y < down_tank_boundary:
                            player.tank = None
                            server.bullet_objects.remove(bullet)
                            break
                    if tank.direction_vector == UP_UNIT_VECTOR or tank.direction_vector == DOWN_UNIT_VECTOR:
                        left_tank_boundary = tank.center[0] - VEHICLE_HEIGHT / 2
                        right_tank_boundary = tank.center[0] + VEHICLE_HEIGHT / 2
                        upper_tank_boundary = tank.center[1] - VEHICLE_WIDTH / 2
                        down_tank_boundary = tank.center[1] + VEHICLE_WIDTH / 2
                        if left_tank_boundary < bullet.x < right_tank_boundary and upper_tank_boundary < bullet.y < down_tank_boundary:
                            player.tank = None
                            server.bullet_objects.remove(bullet)
                            break


def ServerHandlingThread(server):
    createBots(server)
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        handleBots(server)
        bulletCollisionCheck(server)
        updateTanks(server)
        createBullets(server)
        updateBullets(server)
