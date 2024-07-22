import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = -10
MAX_JUMPS = 2
COCONUT_WIDTH = 30
COCONUT_HEIGHT = 30
COCONUT_COLOR = (139, 69, 19)
COCONUT_FALL_SPEED = 5
NEW_COCONUT_INTERVAL = 2000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Game with Double Jump and Falling Coconuts')

background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
player_velocity_y = 0
jump_count = 0

coconuts = []
last_coconut_time = pygame.time.get_ticks()

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_SPACE] and jump_count < MAX_JUMPS:
        player_velocity_y = JUMP_STRENGTH
        jump_count += 1

    player_velocity_y += GRAVITY
    player_y += player_velocity_y

    if player_y + PLAYER_HEIGHT > SCREEN_HEIGHT:
        player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
        player_velocity_y = 0
        jump_count = 0

    if player_x < 0:
        player_x = 0
    if player_x + PLAYER_WIDTH > SCREEN_WIDTH:
        player_x = SCREEN_WIDTH - PLAYER_WIDTH
    if player_y < 0:
        player_y = 0

    current_time = pygame.time.get_ticks()
    if current_time - last_coconut_time > NEW_COCONUT_INTERVAL:
        coconut_x = random.randint(0, SCREEN_WIDTH - COCONUT_WIDTH)
        coconuts.append([coconut_x, 0])
        last_coconut_time = current_time

    for coconut in coconuts:
        coconut[1] += COCONUT_FALL_SPEED
        if player_x < coconut[0] < player_x + PLAYER_WIDTH and player_y < coconut[1] < player_y + PLAYER_HEIGHT:
            print("Hit by a coconut!")
            pygame.quit()
            sys.exit()
        elif coconut[1] > SCREEN_HEIGHT:
            coconuts.remove(coconut)

    screen.blit(background, (0, 0))

    screen.blit(player_image, (player_x, player_y))

    for coconut in coconuts:
        pygame.draw.rect(screen, COCONUT_COLOR, (coconut[0], coconut[1], COCONUT_WIDTH, COCONUT_HEIGHT))

    pygame.display.flip()

    clock.tick(30)
