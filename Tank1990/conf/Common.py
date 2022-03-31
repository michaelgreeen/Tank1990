from time import sleep


SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
IP_ADDRESS = "127.0.0.1"
PORT = 5555
VEHICLE_WIDTH = 100
VEHICLE_HEIGHT = 100

GREEN = (0, 255, 0)
RED = (255, 0, 0)

CLIENT_STARTING_POSITIONS = [(0,0), (SCREEN_WIDTH - VEHICLE_WIDTH,0), (0,SCREEN_HEIGHT - VEHICLE_HEIGHT), (SCREEN_WIDTH - VEHICLE_WIDTH, SCREEN_HEIGHT - VEHICLE_HEIGHT)]
STARTING_POS_CLIENT1 = (0,0)
STARTING_POS_CLIENT2 = (SCREEN_WIDTH - VEHICLE_WIDTH,0)
STARTING_POS_CLIENT3 = (0,SCREEN_HEIGHT - VEHICLE_HEIGHT)
STARTING_POS_CLIENT4 = (SCREEN_WIDTH - VEHICLE_WIDTH, SCREEN_HEIGHT - VEHICLE_HEIGHT)


def read_pos_team(str: str):
    print(str)
    str = str.split(",")
    return int(str[0]), int(str[1]), str[2]


def make_pos_team(tup):
    print(str(tup[0]) + "," + str(tup[1]) + "," + tup[2])
    return str(tup[0]) + "," + str(tup[1]) + "," + tup[2]


