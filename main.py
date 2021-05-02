import pygame
import random
import math
from pygame import mixer

pygame.init()  # This is to Initialise the game
screen = pygame.display.set_mode((800, 600))  # create screen and set height

# Background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):  # This function is used to display the value on the screen
    screen.blit(playerImg, (x, y))  # Blit is used to display stuff on the screen


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("invader.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):  # This function is used to display the value on the screen
    screen.blit(enemyImg[i], (x, y))  # Blit is used to display stuff on the screen


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # Ready state means bullet has not yet been fired, we use this as a bool

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 16)
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    over_text = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


enemy_image = pygame.image.load("invader.png")


def resetGame():
    global playerX, playerY, playerX_change
    global enemyImg, enemyX, enemyY, enemyX_change, enemyY_change
    global score_value
    global bulletX, bulletY, bulletX_change, bulletY_change, bullet_state

    playerX = 370
    playerY = 480
    playerX_change = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6
    for i in range(num_of_enemies):
        enemyImg.append(enemy_image)
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    score_value = 0


# Game Loop
running = True
while running:

    # Background color
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # pygame.event.get() function is used to create a container of every action done
        if event.type == pygame.QUIT:  # Close game when cross is clicked
            running = False

        # Recording Keystrokes
        if event.type == pygame.KEYDOWN:  # KEYDOWN is used to check if key is pressed
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:  # Bullet Shot
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)
            if event.key == pygame.K_r:
                resetGame()

        if event.type == pygame.KEYUP:  # KEYUP is used to know if the key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player Call
    playerX += playerX_change

    # Setting Boundaries
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY += enemyY_change

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            score_value += 1
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    # Constantly updates the changes
    pygame.display.update()
