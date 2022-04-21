from time import sleep


SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
IP_ADDRESS = "127.0.0.1"
PORT = 5555
VEHICLE_WIDTH = 100
VEHICLE_HEIGHT = 100
VEHICLE_VELOCITY = 10
BULLET_CALIBER = 10
BULLET_LENGTH = 20
BULLET_VELOCITY = 30

GREEN = (0, 255, 0)
RED = (255, 0, 0)

CLIENT_STARTING_POSITIONS = [(0,0), (SCREEN_WIDTH - VEHICLE_WIDTH,0), (0,SCREEN_HEIGHT - VEHICLE_HEIGHT), (SCREEN_WIDTH - VEHICLE_WIDTH, SCREEN_HEIGHT - VEHICLE_HEIGHT)]

UP_UNIT_VECTOR = (0, -1)
DOWN_UNIT_VECTOR = (0, 1)
LEFT_UNIT_VECTOR = (-1, 0)
RIGHT_UNIT_VECTOR = (1, 0)
CLIENT_STARTING_DIRECTION_VECTOR = [(1, 0), (1,0), (-1, 0), (-1, 0)]


def read_pos_team(string: str):
    string = string.split(",")
    return int(string[0]), int(string[1]), string[2]


def make_pos_team(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])


