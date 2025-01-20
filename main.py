import pygame
import random
import math
import os, sys
from pygame import mixer

# First, install pyinstaller.
# Open Windows Command Prompt, type:
# pip install pyinstaller
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# rozpocznij program
pygame.init()

# Wynik
score = 0

font_url = resource_path("assets/fonts/Micro5-Regular.ttf")
# font = pygame.font.Font("freesansbold.ttf", 32) # ładowanie czcionki wbudowanej w pygame
font = pygame.font.Font(font_url, 32) # czcionka z fonts.google.com
textX = 10
textY = 10

# sword-stab-pull-melee-weapon-236207.mp3
# Sound Effect by Cyberwave Orchestra from Pixabay

# failure-1-89170.mp3
# hurry-95692.mp3
# Sound Effect by freesound_community from Pixabay

# dźwięk tła
music_url = resource_path("sounds/hurry-95692.mp3")
mixer.music.load(music_url)
mixer.music.play(-1) # oznacza odtwarzanie w pętli
mixer.music.set_volume(0.30) # głośność 0-1

# game over dźwięk
# over_sound = mixer.Sound("sounds/failure-1-89170.wav")

def show_score(x, y):
    scoreText = font.render(f"Wynik: {score}", True, (0,0,0))
    screen.blit(scoreText, (x, y))

# dirtyRect = [] # "kwadraty" które mają się odświeżać

clockGame = pygame.time.Clock() # zmienna zawiera zczytany czas systemowy

# stwórz ekran gry
screen = pygame.display.set_mode((800, 600)) # szerokość i wysokość okna

# nazwa gry
pygame.display.set_caption("SuperGra")

# ikona gry
icon_url =  resource_path("assets/swords_32.png")
icon = pygame.image.load(icon_url).convert_alpha()
pygame.display.set_icon(icon)

# gracz
player_url = resource_path("assets/viking_64.png")
playerImg = pygame.image.load(player_url).convert_alpha()
playerX = 368 # całość ma (800) / 2 - szerokość obrazka  (64) / 2
playerY = 480
speedX = 0
speedY = 0
playerSpeedChange = 3

# przeciwnik 1
enemyImg = []
enemyX = []
enemyY = []
enemySpeedX = []
numOfEnemies = 6
for i in range(numOfEnemies):
    enemy_url = resource_path("assets/ninja_64.png")
    enemyImg.append(pygame.image.load(enemy_url).convert_alpha())
    enemyX.append(random.randint(1, 735))  # dla bezpieczeństwa zmieniamy z 0 na 1 i z 736 na 735
    enemyY.append(0)  # pokaże się na górze ekranu
    enemySpeedX.append(random.choice([-3, -2, -1, 1, 2, 3]))  # wybór prędkości i kierunku z listy (nie może być 0)

# strzał
sword_url = resource_path("assets/sword_32.png")
swordImg = pygame.image.load(sword_url).convert_alpha()
swordX = -50 # nie może być 0 bo czasem wykryje kolizję przed wystrzałem
swordY = -50 # nie może być 0 bo czasem wykryje kolizję przed wystrzałem
swordSpeedY = 5
swordState = "ready" # ready / throw

# koniec gry
gameState = "play" # satus gry potrzebny do jej wznowienia play / over
over_font = pygame.font.Font(font_url, 70)
def game_over():
    global gameState, numOfEnemies, enemyY
    gameState = "over"
    for j in range(numOfEnemies):
        enemyY[j] = 2000  # usuwamy resztę przeciwników
    overText = over_font.render(f"GAME OVER! Wynik: {score}", True, (255, 0, 0))
    # centrowanie tekstu
    textRect = overText.get_rect()
    textRect.center = (800 // 2, 600 // 2)
    screen.blit(overText, textRect)

# nowa gra
def new_game():
    global gameState, score, playerX, playerY
    gameState = "play"
    score = 0
    for i in range(numOfEnemies):
        gen_enemy(i)
    playerX = 368
    playerY = 480

def player(x, y):
    screen.blit(playerImg, (x, y))  # rysuje gracza
    # r = screen.blit(playerImg, (x, y)) # rysuje gracza i dodaje do zmiennej "r"
    # global dirtyRect # odwołanie do zmiennej poza funkcją
    # dirtyRect.append(r) # dodajemy zmienną do listy odświeżania

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # rysuje przeciwnika 1
    # r = screen.blit(enemyImg[i], (x, y)) # rysuje przeciwnika 1
    # global dirtyRect  # odwołanie do zmiennej poza funkcją
    # dirtyRect.append(r)  # dodajemy zmienną do listy odświeżania

def throw_sword(x, y):
    global swordState # odwołanie do zmiennej poza funkcją
    swordState = "throw"
    screen.blit(swordImg, (x + 16, y + 10))  # rysuje miecz
    # r = screen.blit(swordImg, (x + 16, y + 10)) # rysuje miecz
    # global dirtyRect  # odwołanie do zmiennej poza funkcją
    # dirtyRect.append(r)  # dodajemy zmienną do listy odświeżania

def is_collision(enemyX, enemyY, swordX, swordY, d):
    distance = math.sqrt((math.pow(enemyX - swordX, 2) + math.pow(enemyY - swordY, 2))) # wzór na odległość punktów
    if distance < d:
        return True
    else:
        return False
def gen_enemy(i): # znika i pojawia się na górze
    global enemyX, enemyY, enemySpeedX
    enemyX[i] = random.randint(1, 735)
    enemyY[i] = 0
    enemySpeedX[i] = random.choice([-3, -2, -1, 1, 2, 3])

throw_sound_url = resource_path("sounds/sword-stab-pull-melee-weapon-236207.wav")
death_sound_url = resource_path("sounds/grunt2-85989.wav")
running = True
while running:
    screen.fill((109,226,73)) # kolor tła

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # wyjście z gry
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # strzał spacją
                if swordState == "ready": # jeden strzał
                    throw_sound = mixer.Sound(throw_sound_url)
                    throw_sound.play()
                    swordY = playerY
                    swordX = playerX
                    throw_sword(swordX, swordY)
            if gameState == "over":
                if event.key == pygame.K_r: # r jak reset
                    new_game()



    # poprawiony ruch klawiatury
    keys = pygame.key.get_pressed() # wykrywa wszystkie przyciski aktualnie przycisniete

    speedX = 0 # wyzerowanie prędkości przy każdym wywolaniu petli
    speedY = 0

    if gameState == "play":
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

    # ogranicz obszar ruchu dla przeciwnika 1
    for i in range(numOfEnemies):
        if enemyY[i] > 536: # jeżeli którykolwiek przeciwnik dotknie dołu ekranu
            game_over()
            # over_sound.play()
            break

        if enemyX[i] <= 0:
            enemySpeedX[i] *= -1 # jak dojdzie do krawędzi to zmieni kierunek
            enemyY[i] += 32 # i przesunie się w dol
        elif enemyX[i] >= 736: # 800 - 64
            enemySpeedX[i] *= -1
            enemyY[i] += 32

        # kolizja przeciwnik - miecz
        collision = is_collision(enemyX[i], enemyY[i], swordX, swordY, 25)
        if collision:
            death_sound = mixer.Sound(death_sound_url)
            death_sound.play()
            swordState = "ready"  # resetujemy miecz
            swordY = -50  # i usuwamy go z ekranu
            score += 1  # dodajemy punkt
            gen_enemy(i)
        enemy(enemyX[i], enemyY[i], i) # generujemy przeciwnika 1

        # kolizja przeciwnik - gracz
        playerColision = is_collision(enemyX[i], enemyY[i], playerX, playerY, 60)
        if playerColision:
            game_over()
            # over_sound.play()
            break

        enemyX[i] += enemySpeedX[i]

    if swordY <= -32: # jeżeli strzała poza planszą
        swordState = "ready"

    # strzał
    if swordState == "throw":
        throw_sword(swordX,swordY)
        swordY -= swordSpeedY

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.flip() # odświeża caly ekran
    # pygame.display.update(dirtyRect) # odświeża konkretne obszary dodane do zmiennej (listy) - nie działa na openGL
    clockGame.tick(60) # poprawne odtwarzanie w 60 klatkach na sekunde
