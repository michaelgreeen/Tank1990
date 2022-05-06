from time import sleep


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
IP_ADDRESS = "127.0.0.1"
PORT = 5555
VEHICLE_WIDTH = 80.0
VEHICLE_HEIGHT = 80.0
VEHICLE_VELOCITY = 10.0
BARREL_CALIBER = 16.0
BARREL_LENGTH = 25.0
BULLET_CALIBER = 6.0
BULLET_LENGTH = 10.0
BULLET_VELOCITY = 25.0
DOWN_BARREL_HORIZONTAL_OFFSET = -5.0
DOWN_BARREL_VERTICAL_OFFSET = -5.0
UP_BARREL_HORIZONTAL_OFFSET = -5.0
UP_BARREL_VERTICAL_OFFSET = -25.0
LEFT_BARREL_HORIZONTAL_OFFSET = -25.0
LEFT_BARREL_VERTICAL_OFFSET = -6.0
RIGHT_BARREL_HORIZONTAL_OFFSET = -8.0
RIGHT_BARREL_VERTICAL_OFFSET = -12.0
MAP_ROWS = 10
MAP_COLUMNS = 10
INTERVAL_HORIZONTAL = SCREEN_WIDTH/MAP_COLUMNS
INTERVAL_VERTICAL = SCREEN_HEIGHT/MAP_ROWS



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


