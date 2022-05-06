import pickle

import pygame

from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Bullet.Bullet import Bullet


class Tank:
    def __init__(self, x, y, direction_vector, color):
        self.x: int = x
        self.y: int = y
        self.width: int = VEHICLE_WIDTH
        self.height: int = VEHICLE_HEIGHT
        self.vel: int = VEHICLE_VELOCITY
        self.color = color
        self.direction_vector = direction_vector
        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.barrel_attachement_coord = list(self.center)
        self.shooting_cooldown = 0
        self.body_img_path = ""
        self.barrel_img_path = ""
        self.onSand = False
        if color == RED:
            self.body_img_path = "tankRed_outline.png"
            self.barrel_img_path = "barrelRed_outline.png"
        elif color == GREEN:
            self.body_img_path = "tankGreen_outline.png"
            self.barrel_img_path = "barrelGreen_outline.png"


    def draw(self, win):
        body_img = pygame.image.load("..\\img\\" + self.body_img_path).convert()
        barrel_img = pygame.image.load("..\\img\\" + self.barrel_img_path).convert()

        if self.direction_vector == DOWN_UNIT_VECTOR:
            body_img = pygame.transform.rotate(body_img, 180)
            barrel_img = pygame.transform.rotate(barrel_img, 180)
            self.barrel_attachement_coord[0] += DOWN_BARREL_HORIZONTAL_OFFSET
            self.barrel_attachement_coord[1] += DOWN_BARREL_VERTICAL_OFFSET
        elif self.direction_vector == RIGHT_UNIT_VECTOR:
             body_img = pygame.transform.rotate(body_img, -90)
             barrel_img = pygame.transform.rotate(barrel_img, -90)
             self.barrel_attachement_coord[0] += RIGHT_BARREL_HORIZONTAL_OFFSET
             self.barrel_attachement_coord[1] += RIGHT_BARREL_VERTICAL_OFFSET
        elif self.direction_vector == LEFT_UNIT_VECTOR:
             body_img = pygame.transform.rotate(body_img, 90)
             barrel_img = pygame.transform.rotate(barrel_img, 90)
             self.barrel_attachement_coord[0] += LEFT_BARREL_HORIZONTAL_OFFSET
             self.barrel_attachement_coord[1] += LEFT_BARREL_VERTICAL_OFFSET
        else:
             self.barrel_attachement_coord[0] += UP_BARREL_HORIZONTAL_OFFSET
             self.barrel_attachement_coord[1] += UP_BARREL_VERTICAL_OFFSET
        body_img = pygame.transform.scale(body_img,(VEHICLE_WIDTH,VEHICLE_HEIGHT))
        barrel_img = pygame.transform.scale(barrel_img,(BARREL_LENGTH,BARREL_CALIBER))
        win.blit(body_img, (self.x, self.y))
        win.blit(barrel_img, self.barrel_attachement_coord)

    def checkMovingCollision(self, mapOutline,prevX,prevY):
        conditionRight = float(self.x + self.width)
        conditionLeft = float(self.x - self.vel - self.width)
        conditionUp = float(self.y - self.vel - self.height)
        conditionDown = float(self.y + self.height)

        for i in range(MAP_ROWS):
            for j in range(MAP_COLUMNS):
                if conditionRight >= INTERVAL_HORIZONTAL*j+1\
                    and conditionLeft <= INTERVAL_HORIZONTAL*j+1\
                    and conditionDown >= INTERVAL_VERTICAL*i+1\
                    and conditionUp <= INTERVAL_VERTICAL * i+1:
                    if mapOutline[i][j] == 0:
                        self.vel = VEHICLE_VELOCITY
                    elif mapOutline[i][j] == 2:
                        self.vel = VEHICLE_VELOCITY/2
                    elif mapOutline[i][j] == 4:
                        self.vel = VEHICLE_VELOCITY*2
                    else:
                        self.x = prevX
                        self.y = prevY




    def move(self, vector,mapOutline):
        if vector == LEFT_UNIT_VECTOR and (self.x - self.vel >= 0):
            self.x -= self.vel
            self.direction_vector = LEFT_UNIT_VECTOR
            self.checkMovingCollision(mapOutline,self.x + self.vel,self.y)
        if vector == RIGHT_UNIT_VECTOR and (self.x + self.width + self.vel <= SCREEN_WIDTH):
            self.x += self.vel
            self.direction_vector = RIGHT_UNIT_VECTOR
            self.checkMovingCollision(mapOutline,self.x - self.vel,self.y)
        if vector == UP_UNIT_VECTOR and (self.y - self.vel >= 0):
            self.y -= self.vel
            self.direction_vector = UP_UNIT_VECTOR
            self.checkMovingCollision(mapOutline,self.x, self.y + self.vel)
        if vector == DOWN_UNIT_VECTOR and (self.y + self.height + self.vel <= SCREEN_HEIGHT):
            self.y += self.vel
            self.direction_vector = DOWN_UNIT_VECTOR
            self.checkMovingCollision(mapOutline,self.x, self.y- self.vel)
        self.update()


    def update(self):
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1
        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.barrel_attachement_coord = list(self.center)


    def shoot(self):
        if self.shooting_cooldown == 0:
            self.shooting_cooldown = 30
            return Bullet(self.barrel_attachement_coord[0], self.barrel_attachement_coord[1], BULLET_CALIBER, BULLET_LENGTH, self.direction_vector, self.color)
        else:
            return

    def serializeTank(self):
        return pickle.dumps(self)
