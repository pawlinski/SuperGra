import pygame
import random

from pygame.examples.go_over_there import clock

# rozpocznij program
pygame.init()
clock = pygame.time.Clock() # zmienna zawiera zczytany czas systemowy

# stwórz ekran gry
screen = pygame.display.set_mode((800, 600)) # szerokość i wysokość okna

# nazwa gry
pygame.display.set_caption("SuperGra")

# ikona gry
icon = pygame.image.load("assets/swords_32.png")
pygame.display.set_icon(icon)

# gracz
playerImg = pygame.image.load("assets/viking_64.png")
playerX = 368 # całość ma (800) / 2 - szerokość obrazka  (64) / 2
playerY = 480
speedX = 0
speedY = 0

# przeciwnik 1
enemyImg = pygame.image.load("assets/ninja_64.png")
enemyX = random.randint(0, 736) # całość ma (800) / 2 - szerokość obrazka  (64) / 2
enemyY = random.randint(20, 250)
enemySpeedX = 1

def player(x, y):
    screen.blit(playerImg, (x, y)) # rysuje gracza

def enemy(x, y):
    screen.blit(enemyImg, (x, y)) # rysuje przeciwnika 1

running = True
while running:
    screen.fill((109,226,73)) # kolor tła

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # wyjście z gry
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         speedX = -0.3
        #     if event.key == pygame.K_RIGHT:
        #         speedX = 0.3
        #     if event.key == pygame.K_UP:
        #         speedY = -0.3
        #     if event.key == pygame.K_DOWN:
        #         speedY = 0.3
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHTevent.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #         speedX = 0
        #         speedY = 0
    # poprawiony ruch klawiatury
    keys = pygame.key.get_pressed() # wykrywa wszystkie przyciski aktualnie przycisniete

    speedX = 0 # wyzerowanie prędkości przy każdym wywolaniu petli
    speedY = 0

    if keys[pygame.K_LEFT]:
        speedX = -3
    elif keys[pygame.K_RIGHT]:
        speedX = 3

    if keys[pygame.K_UP]:
        speedY = -3
    elif keys[pygame.K_DOWN]:
        speedY = 3

    playerX += speedX
    playerY += speedY

    # ogranicz obszar gry dla gracza
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736: # 800 - 64
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536: # 600 - 64
        playerY = 536

    # ognanicz obszar ruchu dla przeciwnika 1
    if enemyX <= 0:
        enemySpeedX *= -1 # jak dojdzie do krawędzi to zmieni kierunek
        enemyY += 32 # i przesunie się w dol
    elif enemyX >= 736: # 800 - 64
        enemySpeedX *= -1
        enemyY += 32

    enemyX += enemySpeedX

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.flip() # odswierza caly ekran
    clock.tick(60) # poprawne odtwarzanie w 60 klatkach na sekunde
