import pygame
import random
import math

from pygame.examples.go_over_there import clock

# rozpocznij program
pygame.init()

score = 0
# dirtyRect = [] # "kwadraty" które mają się odświeżać

clockGame = pygame.time.Clock() # zmienna zawiera zczytany czas systemowy

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
playerSpeedChange = 3

# przeciwnik 1
enemyImg = pygame.image.load("assets/ninja_64.png")
enemyX = random.randint(1, 735)  # dla bezpieczeństwa zmieniamy z 0 na 1 i z 736 na 735
enemyY = 0  # pokaże się na górze ekranu
enemySpeedX = random.choice([-3, -2, -1, 1, 2, 3])  # wybór prędkości i kierunku z listy (nie może być 0)

# strzał
swordImg = pygame.image.load("assets/sword_32.png")
swordX = 0
swordY = 0
swordSpeedY = 5
swordState = "ready" # ready / throw

def player(x, y):
    screen.blit(playerImg, (x, y))  # rysuje gracza
    # r = screen.blit(playerImg, (x, y)) # rysuje gracza i dodaje do zmiennej "r"
    # global dirtyRect # odwołanie do zmiennej poza funkcją
    # dirtyRect.append(r) # dodajemy zmienną do listy odświeżania

def enemy(x, y):
    screen.blit(enemyImg, (x, y))  # rysuje przeciwnika 1
    # r = screen.blit(enemyImg, (x, y)) # rysuje przeciwnika 1
    # global dirtyRect  # odwołanie do zmiennej poza funkcją
    # dirtyRect.append(r)  # dodajemy zmienną do listy odświeżania

def throw_sword(x, y):
    global swordState # odwołanie do zmiennej poza funkcją
    swordState = "throw"
    screen.blit(swordImg, (x + 16, y + 10))  # rysuje miecz
    # r = screen.blit(swordImg, (x + 16, y + 10)) # rysuje miecz
    # global dirtyRect  # odwołanie do zmiennej poza funkcją
    # dirtyRect.append(r)  # dodajemy zmienną do listy odświeżania

def is_collision(enemyX, enemyY, swordX, swordY):
    distance = math.sqrt(math.pow(enemyX - swordX, 2) + math.pow(enemyY - swordY, 2)) # wzór na odległość punktów
    if distance < 25:
        return True
    else:
        return False
def gen_enemy():
    global enemyX, enemyY, enemySpeedX
    enemyX = random.randint(1, 735)
    enemyY = 0
    enemySpeedX = random.choice([-3, -2, -1, 1, 2, 3])


running = True
while running:
    screen.fill((109,226,73)) # kolor tła

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # wyjście z gry
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # strzał spacją
                if swordState == "ready": # jeden strzał
                    swordY = playerY
                    swordX = playerX
                    throw_sword(swordX, swordY)

    # poprawiony ruch klawiatury
    keys = pygame.key.get_pressed() # wykrywa wszystkie przyciski aktualnie przycisniete

    speedX = 0 # wyzerowanie prędkości przy każdym wywolaniu petli
    speedY = 0

    if keys[pygame.K_LEFT]:
        speedX = -playerSpeedChange
    elif keys[pygame.K_RIGHT]:
        speedX = playerSpeedChange

    if keys[pygame.K_UP]:
        speedY = -playerSpeedChange
    elif keys[pygame.K_DOWN]:
        speedY = playerSpeedChange

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

    if swordY <= -32: # jeżeli strzała poza planszą
        swordState = "ready"

    # strzał
    if swordState == "throw":
        throw_sword(swordX,swordY)
        swordY -= swordSpeedY

    # kolizja
    collision = is_collision(enemyX, enemyY, swordX, swordY)
    if collision:
        swordState = "ready" # resetujemy miecz
        swordY = -50 # i usuwamy go z ekranu
        score += 1 # dodajemy punkt
        gen_enemy()

    enemy(enemyX, enemyY)

    pygame.display.flip() # odświeża caly ekran
    # pygame.display.update(dirtyRect) # odświeża konkretne obszary dodane do zmiennej (listy) - nie działa na openGL
    clockGame.tick(60) # poprawne odtwarzanie w 60 klatkach na sekunde
