import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("First Pygame window")
icon = pygame.image.load("D:\program files\Python projects\Codes\pygame_icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("D:\program files\Python projects\Codes\pygame_backgourn.jpg")
# mixer.music.load()
# mixer.music.play(-1)

player = pygame.image.load("D:\program files\Python projects\Codes\pygame_space-ship.png")
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("D:\program files\Python projects\Codes\pygame_pixels-alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(1)
    enemyY_change.append(20)

bullet = pygame.image.load("D:\program files\Python projects\Codes\pygame_bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.3
bullet_state = "ready"

score_val = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

game_over_font = pygame.font.Font("freesansbold.ttf", 62)


def Score(x, y):
    score = font.render("Score : " + str(score_val), True, (0, 150, 150))
    screen.blit(score, (x, y))


def Player(x, y):
    screen.blit(player, (x, y))


def Enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def Bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


def Collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over():
    game_over_text = game_over_font.render("Game Over" , True, (0, 150, 150))
    screen.blit(game_over_text, (200, 250))


run = True
while run:
    screen.fill((0, 150, 150))  # this is a damn good color
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                playerX_change = 1.3

            if event.key == pygame.K_LEFT:
                playerX_change = -1.3

            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("D:\program files\Python projects\Codes\pygame_laser.mp3")
                bullet_sound.play()
                if bullet_state == "ready":
                    bulletX = playerX
                    Bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_enemies):
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        collision = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == True:  # if collision:
            expl_sound = mixer.Sound("D:\program files\Python projects\Codes\pygame_explosion.wav")
            expl_sound.play()
            bullet_state = "ready"
            bulletY = playerY  # bulletY = 480
            score_val += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 200)

        Enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        Bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    playerX += playerX_change
    Score(textX, textY)
    Player(playerX, playerY)
    pygame.display.update()  # this updates the display after we have added command
