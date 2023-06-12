import objects
import os
import pygame
import random

import Levels
import cards

pygame.init()

WIDTH = 1280
HEIGHT = 720
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

CLICKED_DICES = 0

running = True


path = 'images'
# path = os.path.join(os.pardir, 'images')
file_names = sorted(os.listdir(path))
BACKGROUND = pygame.image.load(os.path.join(path, 'background.jpg')).convert()
# file_names.remove('background.jpg')
IMAGES = {}
for file_name in file_names:
    IMAGES[file_name[:-4].upper()] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)

set_of_dices = pygame.sprite.Group()
set_of_cards = pygame.sprite.Group()

DICES = [IMAGES["DICE1"], IMAGES["DICE2"], IMAGES["DICE3"],
         IMAGES["DICE4"], IMAGES["DICE5"], IMAGES["DICE6"], ]


enemy1 = objects.Fighter("E1", [IMAGES["ENEMY1"], IMAGES["ENEMY2"]], 1280 - 80, 100)
enemy2 = objects.Fighter("E2", [IMAGES["ENEMY1"], IMAGES["ENEMY2"]], 1280 - 80, 100)
enemy3 = objects.Fighter("E3", [IMAGES["ENEMY1"], IMAGES["ENEMY2"]], 1280 - 80, 100)

player = objects.Fighter("Player", [IMAGES["PLAYER1"], IMAGES["PLAYER2"]], 80, 720 - 100)

# Menu start:
m_start = Levels.Menu(BACKGROUND, IMAGES, "Start")
# Menu pause:
m_pause = Levels.Menu(BACKGROUND, IMAGES, "Continue")
# Poziom pierwszy:
l_one = Levels.Level(player, enemy1, BACKGROUND, IMAGES)
# Poziom drugi:
l_two = Levels.Level(player, enemy2, BACKGROUND, IMAGES)
# Poziom trzeci:
l_three = Levels.Level(player, enemy3, BACKGROUND, IMAGES)


dice_spawn_x = 300
dice_spawn_y = HEIGHT + 70


current_level = l_one
player.level = current_level
enemy1.level = current_level

attack_card = cards.DiceCard([IMAGES["KARTA1"], IMAGES["KARTA1GRAY"]], 250, 300, player)
current_level.set_of_cards.add(attack_card)
attack_card.level = current_level

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current_level = m_pause
            elif event.key == pygame.K_SPACE:
                if player.dices > 0:
                    d = objects.Dice(DICES, dice_spawn_x, dice_spawn_y, random.randint(0, 5))
                    current_level.set_of_dices.add(d)
                    dice_spawn_x += 100
                    player.dices -= 1

    key_pressed = pygame.event.get()

    option = current_level.update()
    if option == 'b1':
        current_level = l_one
    elif option == 'bq':
        running = False
    elif option == 'nt':
        for dice in current_level.set_of_dices:
            dice.kill()
        for card in current_level.set_of_cards:
            card.image = card.images[0]
            # card.kill()
        current_level.player.dices = current_level.player.max_dices
        dice_spawn_x = 300

    current_level.draw(screen)

    pygame.display.flip()
    timer.tick(fps)

pygame.quit()
