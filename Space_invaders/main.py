import pygame
import random
import math
from pygame import mixer

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load('background.ogg')
mixer.music.play(-1)

# Title
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

nums_of_enemies = 6
enemy_size = 48   # spacing reference

# helper: avoid overlap spawn
def spawn_enemy_positions(count):
    positions = []
    attempts = 0

    while len(positions) < count and attempts < 1000:
        x = random.randint(0, 735)
        y = random.randint(50, 150)

        ok = True
        for px, py in positions:
            dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
            if dist < 70:   # spacing gap
                ok = False
                break

        if ok:
            positions.append((x, y))

        attempts += 1

    return positions


spawned = spawn_enemy_positions(nums_of_enemies)

for i in range(nums_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(spawned[i][0])
    enemyY.append(spawned[i][1])
    enemyX_change.append(random.choice([-1, 1]))
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('NATOOR.ttf', 30)
textX = 10
textY = 10

over_font = pygame.font.Font('NATOOR.ttf', 60)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (210, 210))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(ex, ey, bx, by):
    distance = math.sqrt((ex - bx) ** 2 + (ey - by) ** 2)
    return distance < 27


# Game loop
running = True
while running:
    screen.fill((128, 128, 128))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    playerX = max(0, min(playerX, 735))

    # Enemy movement
    for i in range(nums_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(nums_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            collision_sound = mixer.Sound('collision.mp3')
            collision_sound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value += 10

            # respawn without overlap
            new_pos = spawn_enemy_positions(1)[0]
            enemyX[i] = new_pos[0]
            enemyY[i] = new_pos[1]

            enemyX_change[i] = random.choice([-1, 1])

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()