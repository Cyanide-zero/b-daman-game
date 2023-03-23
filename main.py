import pygame
import random

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set the width and height of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
textfont = pygame.font.SysFont("montserrat", 50)

# Set the caption of the game window
pygame.display.set_caption("Simple 2D Shooting Game")

# Define colors
white = (255, 237, 230)
black = (0, 0, 0)
red = (255, 0, 0)

# Define the player
player_width = 50
player_height = 50
player_x = screen_width / 2 - player_width / 2
player_y = screen_height - player_height - 10
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

#bullet
bullet_count = 5
bullet_radius = 10
bullet_speed = 10
bullet_list = []
bullet_color = (0, 104, 255)

#enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemy_list = []

#ammo
ammo_width = 30
ammo_height = 30
ammo_speed = 3
ammo_list = []

# Define the game clock
clock = pygame.time.Clock()

# Define the destroyed enemy count
destroyed_count = 0

# Define the game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_count >= 1:
                bullet_x = player.x + player_width / 2
                bullet_y = player_y
                bullet = pygame.Rect(bullet_x, bullet_y, 2*bullet_radius, 2*bullet_radius)
                bullet_list.append(bullet)
                bullet_count -= 1

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    elif keys[pygame.K_RIGHT] and player.x < screen_width - player_width:
        player.x += player_speed

    # Move the bullets
    for bullet in bullet_list:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullet_list.remove(bullet)

    # Spawn a new enemy
    if len(enemy_list) < 10:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = random.randint(-screen_height, -enemy_height)
        enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        enemy_list.append(enemy)
    # Spawn ammo
    if len(ammo_list) < 2:
        ammo_x = random.randint(0, screen_width - ammo_width)
        ammo_y = random.randint(-screen_height, -ammo_height)
        ammo = pygame.Rect(ammo_x, ammo_y, ammo_width, ammo_height)
        ammo_list.append(ammo)

    # Move the enemies
    for enemy in enemy_list:
        enemy.y += enemy_speed
        if enemy.y > screen_height:
            enemy_list.remove(enemy)
    
    # Move the enemies
    for ammo in ammo_list:
        ammo.y += ammo_speed
        if ammo.y > screen_height:
            ammo_list.remove(ammo)

    # Check for collisions between bullets and enemies
    for bullet in bullet_list:
        for enemy in enemy_list:
            if bullet.colliderect(enemy):
                bullet_list.remove(bullet)
                enemy_list.remove(enemy)
                destroyed_count += 1  # increment destroyed count

    # Check for collisions between player and enemies
    for enemy in enemy_list:
        if player.colliderect(enemy):
            game_over = True

    for ammo in ammo_list:
        if player.colliderect(ammo):
            ammo_list.remove(ammo)
            bullet_count += 1

    # Draw the game objects
    screen.fill(white)
    pygame.draw.rect(screen, black, player)
    for bullet in bullet_list:
        pygame.draw.circle(screen, bullet_color, (bullet.x + bullet_radius, bullet.y + bullet_radius), bullet_radius)
    for enemy in enemy_list:
        pygame.draw.rect(screen, black, enemy)
    for ammo in ammo_list:
        pygame.draw.rect(screen, red, ammo)
    score = textfont.render(str(destroyed_count), 1, (0,0,0))
    screen.blit(score, (390,10))
    ammo = textfont.render(str(bullet_count), 1, black)
    no_ammo = textfont.render(str(bullet_count), 1, red)
    if bullet_count >= 1:
        screen.blit(ammo, (750, 550))
    else:
        screen.blit(no_ammo, (750, 550))

    pygame.display.update()


    # Set the game clock tick
    clock.tick(60)

# Quit Pygame
pygame.quit()
