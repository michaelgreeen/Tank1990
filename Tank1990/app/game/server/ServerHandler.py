import pygame
import random
from math import dist, floor
import time

from Tank1990.resources.entity.Effect.ExplosionEffect import ExplosionEffect
from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import SCREEN_WIDTH, SCREEN_HEIGHT, DOWN_UNIT_VECTOR, UP_UNIT_VECTOR, \
    RIGHT_UNIT_VECTOR, LEFT_UNIT_VECTOR, VEHICLE_WIDTH, VEHICLE_HEIGHT, INTERVAL_HORIZONTAL, INTERVAL_VERTICAL, \
    VEHICLE_VELOCITY, MAP_ROWS, MAP_COLUMNS, CLIENT_STARTING_DIRECTION_VECTOR, CLIENT_STARTING_POSITIONS, PLAYER_COUNT, \
    MOVE_DIRECTION_VECTOR
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
    server.message_queues_lock.get("FOLLOW_EVENT_LOCK").acquire()
    playerTankRequestTuple = server.message_queues.get("FOLLOW_EVENT")

    for bot_number in range(PLAYER_COUNT):
        if server.player_slots[bot_number].isBot:
            botMove(bot_number, server, playerTankRequestTuple)
            if random.randint(0, 1000) < 2 and server.player_slots[bot_number].player.tank is not None:
                scanForEnemy(bot_number,server)
    server.message_queues.get("FOLLOW_EVENT").clear()
    server.message_queues_lock.get("FOLLOW_EVENT_LOCK").release()

def scanForEnemy(selfBotNumber, server):
    scanner_tank = server.player_slots[selfBotNumber].player.tank
    for bot_number in range(PLAYER_COUNT):
        enemy_tank = server.player_slots[bot_number].player.tank
        if bot_number == selfBotNumber:
            continue
        if enemy_tank:
            if enemy_tank.color is not scanner_tank.color:
                C = scanner_tank.center
                A = (enemy_tank.x, enemy_tank.y)
                B = (enemy_tank.x + enemy_tank.width, enemy_tank.y + enemy_tank.height)
                if dist(A,C) + dist(C,B) >= dist(A,B):
                    botShoot(bot_number, server)
                    #print(time.time())
                    #print("Found potential shooting target")





def botMove(bot_number, server, playerTankRequestTuple):
    shortestDistance = 1000000
    shortest_index = -1
    bot:Tank = server.player_slots[bot_number].player.tank \
        if server.player_slots[bot_number].player.tank is not None else None

    condition = True if ((playerTankRequestTuple is not None) and (bot is not None)) else False
    for tuple in playerTankRequestTuple:
        if condition:
            if tuple[0] is not None:
                if bot.color == tuple[0].color and tuple[1] is True:
                    # check if distance is lower after movement in some of directions
                    distances = [dist((bot.x + VEHICLE_VELOCITY, bot.y), tuple[0].center),
                                 dist((bot.x - VEHICLE_VELOCITY, bot.y), tuple[0].center),
                                 dist((bot.x, bot.y - VEHICLE_VELOCITY), tuple[0].center),
                                 dist((bot.x, bot.y + VEHICLE_VELOCITY), tuple[0].center)]
                    min_index = distances.index(min(distances))

                    if distances[min_index] < shortestDistance:
                        shortest_index = min_index

    decideOnBotMovement(bot, bot_number, server, shortest_index)


def decideOnBotMovement(bot, bot_number, server, shortest_index):
    if bot is not None:
        movement_timestamp = int(time.time())
        if bot.botLastTimestamp != movement_timestamp:
            tmpVector = random.choice(MOVE_DIRECTION_VECTOR)
            while tmpVector is not bot.direction_vector:
                bot.direction_vector = random.choice(MOVE_DIRECTION_VECTOR)
            bot.botLastTimestamp = movement_timestamp

        if shortest_index == 0:
            addBotMovementToQueue(bot_number, server, vector=RIGHT_UNIT_VECTOR)
        elif shortest_index == 1:
            addBotMovementToQueue(bot_number, server, vector=LEFT_UNIT_VECTOR)
        elif shortest_index == 2:
            addBotMovementToQueue(bot_number, server, vector=UP_UNIT_VECTOR)
        elif shortest_index == 3:
            addBotMovementToQueue(bot_number, server, vector=DOWN_UNIT_VECTOR)
        else:
            addBotMovementToQueue(bot_number, server, vector=bot.direction_vector)


def addBotMovementToQueue(bot_number, server, vector):
    server.message_queues_lock.get("PLAYER_MOVE_LOCK").acquire()
    server.message_queues.get("PLAYER_MOVE").append((bot_number, vector))
    server.message_queues_lock.get("PLAYER_MOVE_LOCK").release()


def botShoot(bot_number, server):
    server.message_queues_lock.get("BULLET_CREATE_LOCK").acquire()
    server.message_queues.get("BULLET_CREATE").append(bot_number)
    server.message_queues_lock.get("BULLET_CREATE_LOCK").release()


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
        if player_tank is None:
            continue
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
        bullet_x_grid = floor(bullet.x / INTERVAL_HORIZONTAL)
        bullet_y_grid = floor(bullet.y / INTERVAL_VERTICAL)
        if bullet.x > SCREEN_WIDTH or bullet.x < 0:
            server.bullet_objects.remove(bullet)
            continue
        if bullet.y > SCREEN_HEIGHT or bullet.y < 0:
            server.bullet_objects.remove(bullet)
            continue
        if not (bullet_x_grid >= MAP_COLUMNS or bullet_x_grid < 0 or bullet_y_grid >= MAP_ROWS or bullet_y_grid < 0):
            if server.mapOutline[bullet_y_grid][bullet_x_grid] == 1 or server.mapOutline[bullet_y_grid][
                bullet_x_grid] == 3:
                server.mapOutline[bullet_y_grid][bullet_x_grid] = 2
                for player_id in server.player_slots:
                    if not server.player_slots[player_id].isBot:
                        server.player_map_events_locks[player_id].acquire()
                        server.player_map_events[player_id].append(ExplosionEffect(bullet.x, bullet.y))
                        server.player_map_events_locks[player_id].release()
                server.bullet_objects.remove(bullet)
                continue

        for player in (server.teams.get("Green").players + server.teams.get("Red").players):
            tank = player.tank
            if tank is not None and bullet is not None:
                if bullet.color != player.team.color:
                    if tank.direction_vector == RIGHT_UNIT_VECTOR or tank.direction_vector == LEFT_UNIT_VECTOR:
                        down_tank_boundary, left_tank_boundary, right_tank_boundary, upper_tank_boundary = calculateTankBoundaries(
                            tank)
                        if left_tank_boundary < bullet.x < right_tank_boundary and upper_tank_boundary < bullet.y < down_tank_boundary:
                            player.tank = None
                            for player_id in server.player_slots:
                                if not server.player_slots[player_id].isBot:
                                    server.player_map_events_locks[player_id].acquire()
                                    server.player_map_events[player_id].append(ExplosionEffect(bullet.x, bullet.y))
                                    server.player_map_events_locks[player_id].release()
                            server.bullet_objects.remove(bullet)
                            break

                    elif tank.direction_vector == UP_UNIT_VECTOR or tank.direction_vector == DOWN_UNIT_VECTOR:
                        down_tank_boundary, left_tank_boundary, right_tank_boundary, upper_tank_boundary = calculateTankBoundaries(
                            tank)
                        if left_tank_boundary < bullet.x < right_tank_boundary and upper_tank_boundary < bullet.y < down_tank_boundary:
                            player.tank = None
                            for player_id in server.player_slots:
                                if not server.player_slots[player_id].isBot:
                                    server.player_map_events_locks[player_id].acquire()
                                    server.player_map_events[player_id].append(ExplosionEffect(bullet.x, bullet.y))
                                    server.player_map_events_locks[player_id].release()
                            server.bullet_objects.remove(bullet)
                            break


def calculateTankBoundaries(tank):
    left_tank_boundary = tank.center[0] - VEHICLE_WIDTH / 2
    right_tank_boundary = tank.center[0] + VEHICLE_WIDTH / 2
    upper_tank_boundary = tank.center[1] - VEHICLE_HEIGHT / 2
    down_tank_boundary = tank.center[1] + VEHICLE_HEIGHT / 2
    return down_tank_boundary, left_tank_boundary, right_tank_boundary, upper_tank_boundary


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
