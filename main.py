import pygame
import random
import math
from pygame import mixer

running = True

# Initializes the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background2.png')
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

# Player
playerImg = pygame.image.load('ship.png')
playerX = 370
playerY = 480
playerMove = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXMove = []
enemyYMove = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 86))
    enemyXMove.append(3)
    enemyYMove.append(-40)

# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
overFont = pygame.font.Font('freesansbold.ttf', 64)


def showScore(x, y):
    score = font.render("Score: %s" % scoreValue, True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameOverText():
    overText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (200, 250))


# Laser
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserYMove = 10
laserState = "ready"


def player(x, y):
    # blit(Image, (X position, Y position))
    screen.blit(playerImg, (x, y))  # blit is to draw


def enemy(x, y, i):
    # blit(Image, (X position, Y position))
    screen.blit(enemyImg[i], (x, y))  # blit is to draw


def fireLaser(x, y):
    global laserState
    laserState = 'fire'
    screen.blit(laserImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2)) + (math.pow(enemyY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
while running:
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it's right or left
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerMove = -3
            elif event.key == pygame.K_RIGHT:
                playerMove = 3
            elif event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT:
                playerMove = 0

            if event.key == pygame.K_SPACE:
                if laserState == 'ready':
                    laserSound = mixer.Sound('laser.wav')
                    laserSound.set_volume(0.1)
                    laserSound.play()
                    laserX = playerX
                    fireLaser(laserX, laserY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and playerMove < 0:
                playerMove = 0
            elif event.key == pygame.K_RIGHT and playerMove > 0:
                playerMove = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerMove

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(numOfEnemies):

        # Game Over
        if enemyY[i] > 200:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText()
            break
        enemyX[i] += enemyXMove[i]
        if enemyX[i] <= 0:
            enemyXMove[i] = 3
            enemyY[i] -= enemyYMove[i]
        elif enemyX[i] >= 736:
            enemyXMove[i] = -3
            enemyY[i] -= enemyYMove[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            collisionSound = mixer.Sound('explosion.wav')
            collisionSound.set_volume(0.1)
            collisionSound.play()
            laserY = 480
            laserState = 'ready'
            scoreValue += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 86)

        enemy(enemyX[i], enemyY[i], i)

    # Laser movement
    if laserY < -10:
        laserState = 'ready'
        laserY = 480
    if laserState == 'fire':
        fireLaser(laserX, laserY)
        laserY -= laserYMove

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
