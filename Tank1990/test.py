from Tank1990.resources.entity.Tank.Tank import Tank
from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Bullet.Bullet import Bullet
import pygame
import pickle

from Tank1990.resources.entity.Team.Team import Team

def main():
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Client")
    running = True
    teams = {"Green": Team("Green", GREEN), "Red": Team("Red", RED)}
    player1 = Player(1)
    teams.get("Green").addPlayer(player1)
    player1.team = teams.get("Green")
    tank1 = Tank(CLIENT_STARTING_POSITIONS[0][0], CLIENT_STARTING_POSITIONS[0][1], VEHICLE_WIDTH, VEHICLE_HEIGHT, CLIENT_STARTING_DIRECTION_VECTOR[0], player1.team.color)
    player1.assignTank(tank1)
    serverPlayers = [player1]
    bulletObjects = []
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        player1.tank.move()
        bullet = player1.tank.shoot()
        if type(bullet) is Bullet:
            bulletObjects.append(bullet)

        win.fill((0, 0, 0))
        for playerInfo in serverPlayers:
            playerInfo.tank.draw(win)
        for bullet in bulletObjects:
            bullet.update()
            if bullet.x > SCREEN_WIDTH or bullet.x < 0 or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                bulletObjects.remove(bullet)
            else:
                bullet.draw(win)
        pygame.display.update()


main()
