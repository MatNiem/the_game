import time

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
action_cooldown = 0

CLICKED_DICES = 0

running = True





path = 'images'
# path = os.path.join(os.pardir, 'images')
file_names = sorted(os.listdir(path))
BACKGROUND = pygame.image.load(os.path.join(path, 'background.png')).convert()
BACKGROUND_MENU = pygame.image.load(os.path.join(path, 'backgroundx.jpg')).convert()
BACKGROUND_2 = pygame.image.load(os.path.join(path, 'background1.jpg')).convert()
# file_names.remove('background.jpg')
IMAGES = {}
for file_name in file_names:
    IMAGES[file_name[:-4].upper()] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)

set_of_dices = pygame.sprite.Group()
set_of_cards = pygame.sprite.Group()

DICES = [IMAGES["DICE1"], IMAGES["DICE2"], IMAGES["DICE3"],
         IMAGES["DICE4"], IMAGES["DICE5"], IMAGES["DICE6"], ]

enemy = objects.Fighter("E0", [pygame.transform.scale_by(IMAGES["ENEMY1"], 5),
                                pygame.transform.scale_by(IMAGES["ENEMY3"], 5)],
                                [pygame.transform.scale_by(IMAGES["ENEMYA1"], 5),
                                pygame.transform.scale_by(IMAGES["ENEMYA2"], 5)], 1280 - 200, 720 - 200)

enemy1 = objects.Fighter("E1", [pygame.transform.scale_by(IMAGES["ENEMY1"], 5),
                                pygame.transform.scale_by(IMAGES["ENEMY2"], 5)],
                                [pygame.transform.scale_by(IMAGES["ENEMYA1"], 5),
                                pygame.transform.scale_by(IMAGES["ENEMYA2"], 5)], 1280 - 200, 720 - 200, dices=2)
enemy2 = objects.Fighter("E2", [pygame.transform.scale_by(IMAGES["ENEMY1"], 5),
                                pygame.transform.scale_by(IMAGES["ENEMY3"], 5)],
                                [pygame.transform.scale_by(IMAGES["ENEMYA1"], 5),
                                pygame.transform.scale_by(IMAGES["ENEMYA2"], 5)], 1280 - 200, 720 - 200, dices=1)
enemy3 = objects.Fighter("E3", [pygame.transform.scale_by(IMAGES["ENEMY1"], 5),
                                pygame.transform.scale_by(IMAGES["ENEMY3"], 5)],
                                [pygame.transform.scale_by(IMAGES["ENEMYA1"], 5),
                                pygame.transform.scale_by(IMAGES["ENEMYA2"], 5)], 1280 - 200, 720 - 200, dices=1)

player = objects.Fighter("Player", [pygame.transform.scale_by(IMAGES["PLAYER1"], 5),
                                    pygame.transform.scale_by(IMAGES["PLAYER2"], 5)],
                                    [pygame.transform.scale_by(IMAGES["PLAYER1"], 5),
                                    pygame.transform.scale_by(IMAGES["PLAYER2"], 5)], 200, 720 - 200)

# Menu start:
m_start = Levels.Menu(BACKGROUND_2, IMAGES, "Start", player, enemy)
# Menu pause:
m_pause = Levels.Menu(BACKGROUND_MENU, IMAGES, "Continue", player, enemy)
# Poziom pierwszy:
l_one = Levels.Level("Level 1", player, enemy1, BACKGROUND, IMAGES)
# Poziom drugi:
l_two = Levels.Level("Level 2", player, enemy2, BACKGROUND, IMAGES)
# Poziom trzeci:
l_three = Levels.Level("Level 3", player, enemy3, BACKGROUND, IMAGES)

l_one.next_level = l_two
l_two.next_level = l_three
l_three.next_level = m_start

dice_spawn_x = 400
dice_spawn_y = HEIGHT + 70

current_level = m_start
last_level = l_one
player.level = current_level
enemy1.level = current_level

attack_card = cards.DiceCard([IMAGES["KARTA1"], IMAGES["KARTA1GRAY"]], 250, 300, player, 1, 0)
heal_card = cards.DiceCard([IMAGES["PLAYER1X"], IMAGES["PLAYER2X"]], 550, 300, player, 0, 1)
player.set_of_cards.add(attack_card)
player.set_of_cards.add(heal_card)
attack_card.level = l_one
heal_card.level = l_one

is_player_turn = True
bot_turn_passed = False
dices_spawned = False
damage_dealing = False
enemy_attacking = False
player_attacking = False
next_turn_screen = False


def spawn_dices(unit, dice_x, to_the_right=True):
    global DICES, dice_spawn_y, current_level
    for i in range(unit.max_dices):
        d = objects.Dice(DICES, dice_x, dice_spawn_y, random.randint(0, 5))
        current_level.set_of_dices.add(d)
        if to_the_right:
            dice_x += 100
        else:
            dice_x -= 100
        unit.dices -= 1


while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current_level = m_pause
            elif event.key == pygame.K_SPACE:
                spawn_dices(player, dice_spawn_x)

    key_pressed = pygame.event.get()

    current_level.draw(screen, enemy_attacking,  player_attacking, is_player_turn)

    # turn handling
    if not (current_level == m_pause and current_level == m_pause):
        if player.life <= 0:
            pygame.draw.rect(screen, (255,0,0), (0,0,1280,720))
            pygame.display.flip()
            pygame.time.wait(1000)
            running = False
        elif current_level.enemy.life <= 0:
            pygame.draw.rect(screen, (0,0,0), (0,0,1280,720))
            pygame.display.flip()
            pygame.time.wait(1000)
            current_level, last_level = current_level.next_level, current_level
            is_player_turn = True
            spawn_dices(player, dice_spawn_x)
            for c in current_level.set_of_cards:
                c.image = c.images[0]

        else:
            if not is_player_turn:
                action_cooldown += 1
                if action_cooldown >= 90:
                    if not dices_spawned:
                        spawn_dices(current_level.enemy, 900, False)
                        dices_spawned = True
                        action_cooldown = 0
                    else:
                        for d in current_level.set_of_dices:
                            player.life -= d.value + 1
                            d.kill()
                            action_cooldown = 0
                            enemy_attacking = True
                            is_player_turn = True
                        dices_spawned = False
                        enemy_attacking = False
                        action_cooldown = 0

            if is_player_turn:
                action_cooldown += 1
                if not dices_spawned:
                    spawn_dices(player, dice_spawn_x)
                    dices_spawned = True
                    action_cooldown = 0
                for d in current_level.set_of_dices:
                    for c in current_level.set_of_cards:
                        if d.rect.colliderect(c.rect) and not d.clicked and c.image == c.images[0]:
                            c.action(current_level.enemy, d.value + 1, 0, d.value + 1)
                            player_attacking = True
                            d.kill()
                            c.image = c.images[1]
                            player_attacking = False

    # handling buttons
    option = current_level.update()
    if option == 'b1':
        current_level, last_level = l_one, current_level
        if last_level == m_start:
            spawn_dices(current_level.player, dice_spawn_x)
    elif option == 'bq':
        running = False
    elif option == 'nt':
        for dice in current_level.set_of_dices:
            dice.kill()
        for card in current_level.set_of_cards:
            card.image = card.images[0]
            # card.kill()
        current_level.player.dices = current_level.player.max_dices
        is_player_turn = False



    pygame.display.flip()
    timer.tick(fps)


pygame.quit()
