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
BACKGROUND_1 = pygame.image.load(os.path.join(path, 'background.png')).convert()
BACKGROUND_MENU = pygame.image.load(os.path.join(path, 'backgroundx.jpg')).convert()
BACKGROUND_2 = pygame.transform.scale_by(pygame.image.load(os.path.join(path, 'background2.jpg')).convert(), 2.5)
BACKGROUND_3 = pygame.transform.scale_by(pygame.image.load(os.path.join(path, 'background3.jpg')).convert(), 2.5)
# file_names.remove('background.jpg')
IMAGES = {}
for file_name in file_names:
    IMAGES[file_name[:-4].upper()] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND_1)

set_of_dices = pygame.sprite.Group()
set_of_cards = pygame.sprite.Group()

DICES = [IMAGES["DICE1"], IMAGES["DICE2"], IMAGES["DICE3"],
         IMAGES["DICE4"], IMAGES["DICE5"], IMAGES["DICE6"]]

PLAYER_IDLE = [pygame.transform.scale_by(IMAGES["PLAYER1"], 5),
               pygame.transform.scale_by(IMAGES["PLAYER2"], 5),
               pygame.transform.scale_by(IMAGES["PLAYER3"], 5),
               pygame.transform.scale_by(IMAGES["PLAYER4"], 5),
               pygame.transform.scale_by(IMAGES["PLAYER5"], 5),
               pygame.transform.scale_by(IMAGES["PLAYER6"], 5),
               pygame.transform.scale_by(IMAGES["PLAYER7"], 5),
               pygame.transform.scale_by(IMAGES["PLAYER8"], 5)]

PLAYER_ATTACK = [pygame.transform.scale_by(IMAGES["PLAYERA1"], 5),
                 pygame.transform.scale_by(IMAGES["PLAYERA2"], 5),
                 pygame.transform.scale_by(IMAGES["PLAYERA3"], 5),
                 pygame.transform.scale_by(IMAGES["PLAYERA4"], 5),
                 pygame.transform.scale_by(IMAGES["PLAYERA5"], 5),
                 pygame.transform.scale_by(IMAGES["PLAYERA6"], 5),
                 pygame.transform.scale_by(IMAGES["PLAYERA7"], 5),
                 pygame.transform.scale_by(IMAGES["PLAYERA8"], 5)]

PLAYER_DEATH = [pygame.transform.scale_by(IMAGES["PLAYERD1"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD2"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD3"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD4"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD5"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD6"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD7"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD8"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD9"], 5),
                pygame.transform.scale_by(IMAGES["PLAYERD10"], 5)]

ENEMY_IDLE = [pygame.transform.scale_by(IMAGES["ENEMY1"], 5),
              pygame.transform.scale_by(IMAGES["ENEMY2"], 5),
              pygame.transform.scale_by(IMAGES["ENEMY3"], 5),
              pygame.transform.scale_by(IMAGES["ENEMY4"], 5),
              pygame.transform.scale_by(IMAGES["ENEMY5"], 5),
              pygame.transform.scale_by(IMAGES["ENEMY6"], 5),
              pygame.transform.scale_by(IMAGES["ENEMY7"], 5),
              pygame.transform.scale_by(IMAGES["ENEMY8"], 5)]

ENEMY_ATTACK = [pygame.transform.scale_by(IMAGES["ENEMYA1"], 5),
                pygame.transform.scale_by(IMAGES["ENEMYA2"], 5),
                pygame.transform.scale_by(IMAGES["ENEMYA3"], 5),
                pygame.transform.scale_by(IMAGES["ENEMYA4"], 5),
                pygame.transform.scale_by(IMAGES["ENEMYA5"], 5),
                pygame.transform.scale_by(IMAGES["ENEMYA6"], 5),
                pygame.transform.scale_by(IMAGES["ENEMYA7"], 5),
                pygame.transform.scale_by(IMAGES["ENEMYA8"], 5)]

BOSS_IDLE = [pygame.transform.scale_by(IMAGES["HEAVYBANDIT_IDLE_0"], 5),
             pygame.transform.scale_by(IMAGES["HEAVYBANDIT_IDLE_1"], 5),
             pygame.transform.scale_by(IMAGES["HEAVYBANDIT_IDLE_2"], 5),
             pygame.transform.scale_by(IMAGES["HEAVYBANDIT_IDLE_3"], 5),
             pygame.transform.scale_by(IMAGES["HEAVYBANDIT_IDLE_0"], 5),
             pygame.transform.scale_by(IMAGES["HEAVYBANDIT_IDLE_1"], 5),
             pygame.transform.scale_by(IMAGES["HEAVYBANDIT_IDLE_2"], 5),
             pygame.transform.scale_by(IMAGES["HEAVYBANDIT_IDLE_3"], 5)]

BOSS_ATTACK = [pygame.transform.scale_by(IMAGES["HEAVYBANDIT_ATTACK_0"], 5),
               pygame.transform.scale_by(IMAGES["HEAVYBANDIT_ATTACK_1"], 5),
               pygame.transform.scale_by(IMAGES["HEAVYBANDIT_ATTACK_2"], 5),
               pygame.transform.scale_by(IMAGES["HEAVYBANDIT_ATTACK_3"], 5),
               pygame.transform.scale_by(IMAGES["HEAVYBANDIT_ATTACK_4"], 5),
               pygame.transform.scale_by(IMAGES["HEAVYBANDIT_ATTACK_5"], 5),
               pygame.transform.scale_by(IMAGES["HEAVYBANDIT_ATTACK_6"], 5),
               pygame.transform.scale_by(IMAGES["HEAVYBANDIT_ATTACK_7"], 5)]

ENEMY_DEATH = [pygame.transform.scale_by(IMAGES["ENEMYD1"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD2"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD3"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD4"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD5"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD6"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD7"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD8"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD9"], 5),
               pygame.transform.scale_by(IMAGES["ENEMYD10"], 5)]

BOSS_DEATH = [pygame.transform.scale_by(IMAGES["HEAVYBANDIT_RECOVER_7"], 5),
              pygame.transform.scale_by(IMAGES["HEAVYBANDIT_RECOVER_6"], 5),
              pygame.transform.scale_by(IMAGES["HEAVYBANDIT_RECOVER_5"], 5),
              pygame.transform.scale_by(IMAGES["HEAVYBANDIT_RECOVER_4"], 5),
              pygame.transform.scale_by(IMAGES["HEAVYBANDIT_RECOVER_3"], 5),
              pygame.transform.scale_by(IMAGES["HEAVYBANDIT_RECOVER_2"], 5),
              pygame.transform.scale_by(IMAGES["HEAVYBANDIT_RECOVER_1"], 5),
              pygame.transform.scale_by(IMAGES["HEAVYBANDIT_RECOVER_0"], 5),
              pygame.transform.scale_by(IMAGES["HEAVYBANDIT_DEATH_0"], 5)]

enemy = objects.Fighter("E0", ENEMY_IDLE, ENEMY_ATTACK, ENEMY_DEATH, WIDTH - 200, HEIGHT - 200)

enemy1 = objects.Fighter("E1", BOSS_IDLE, BOSS_ATTACK, BOSS_DEATH, WIDTH - 200, HEIGHT - 200, dices=1)
enemy2 = objects.Fighter("E2", ENEMY_IDLE, ENEMY_ATTACK, ENEMY_DEATH, WIDTH - 200, HEIGHT - 200, dices=1)
enemy3 = objects.Fighter("E3", ENEMY_IDLE, ENEMY_ATTACK, ENEMY_DEATH, WIDTH - 200, HEIGHT - 200, dices=1)

player = objects.Fighter("Player", PLAYER_IDLE, PLAYER_ATTACK, PLAYER_DEATH, 200, HEIGHT - 200, life=12)

# Menu start:
m_start = Levels.Menu(BACKGROUND_MENU, IMAGES, "Start", player, enemy)
# Menu pause:
m_pause = Levels.Menu(BACKGROUND_MENU, IMAGES, "Continue", player, enemy)
# Poziom pierwszy:
l_one = Levels.Level("Level 1", player, enemy1, BACKGROUND_2, IMAGES)
# Poziom drugi:
l_two = Levels.Level("Level 2", player, enemy2, BACKGROUND_2, IMAGES)
# Poziom trzeci:
l_three = Levels.Level("Level 3", player, enemy3, BACKGROUND_3, IMAGES)

l_one.next_level = l_two
l_two.next_level = l_three
l_three.next_level = m_start

dice_spawn_x = 400
dice_spawn_y = HEIGHT + 70

current_level = m_start
last_level = l_one
player.level = current_level
enemy1.level = current_level

attack_card = cards.DiceCard([pygame.transform.scale_by(IMAGES["A1"], 0.35),
                              pygame.transform.scale_by(IMAGES["A1_BW"], 0.35)], 250, 300, player, 1, 0, True)
heal_card = cards.DiceCard([IMAGES["KARTA2"], IMAGES["KARTA2GRAY"]], 550, 300, player, 0, 1, max_value=4)
player.set_of_cards.add(attack_card)
player.set_of_cards.add(heal_card)
attack_card.level = l_one
heal_card.level = l_one

is_player_turn = True
bot_turn_passed = False
dices_spawned = False
damage_dealing = False
enemy_attacking = False

next_turn_screen = False


def spawn_dices(unit, dice_x, to_the_right=True):
    global DICES, dice_spawn_y, current_level
    amount = unit.dices
    for i in range(amount):
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

    current_level.draw(screen, is_player_turn)

    # turn handling
    if not (current_level == m_pause and current_level == m_pause):
        # Player is dead:
        if player.life <= 0:
            current_level.player.action = 2
            if len(current_level.player.images_d) - 1 != current_level.player.frame_index \
                    and current_level.player.action == 2:
                pass
            else:
                pygame.time.wait(1000)
                pygame.draw.rect(screen, (255, 0, 0), (0, 0, 1280, 720))
                pygame.display.flip()
                pygame.time.wait(1000)
                running = False
        # Enemy is dead:
        elif current_level.enemy.life <= 0:
            current_level.enemy.action = 2
            if len(current_level.enemy.images_d) - 1 != current_level.enemy.frame_index \
                    and current_level.enemy.action == 2:
                pass
            else:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))
                pygame.display.flip()
                pygame.time.wait(1000)
                current_level, last_level = current_level.next_level, current_level
                is_player_turn = True
                spawn_dices(player, dice_spawn_x)
                for c in current_level.set_of_cards:
                    c.image = c.images[0]

        else:
            # Enemy's turn:
            if not is_player_turn:
                action_cooldown += 1
                if action_cooldown >= 90:
                    if not dices_spawned:
                        spawn_dices(current_level.enemy, 900, False)
                        current_level.enemy.dices = current_level.enemy.max_dices
                        dices_spawned = True
                        action_cooldown = 0
                    else:
                        for d in current_level.set_of_dices:
                            player.life -= d.value + 1
                            current_level.enemy.action = 1
                            d.kill()
                            action_cooldown = 0
                            enemy_attacking = True
                            is_player_turn = True
                        dices_spawned = False
                        enemy_attacking = False
                        action_cooldown = 0
            # Player's turn:
            if is_player_turn:
                action_cooldown += 1
                if not dices_spawned:
                    spawn_dices(player, dice_spawn_x)
                    dices_spawned = True
                    action_cooldown = 0
                for d in current_level.set_of_dices:
                    for c in current_level.set_of_cards:
                        if d.rect.colliderect(c.rect) \
                                and not d.clicked \
                                and c.image == c.images[0] \
                                and c.max_value > d.value:
                            if c.action(current_level.enemy, d.value + 1, d.value + 1):
                                dices_spawned = False
                                current_level.player.dices += 1
                            d.kill()
                            c.image = c.images[1]

    # handling buttons
    option = current_level.update()
    if option == 'b1':
        current_level, last_level = l_one, current_level
        if last_level == m_start:
            current_level.player.dices = current_level.player.max_dices
            spawn_dices(current_level.player, dice_spawn_x)
    elif option == 'bq':
        running = False
    elif option == 'nt':
        for dice in current_level.set_of_dices:
            dice.kill()
        for card in current_level.set_of_cards:
            card.image = card.images[0]
        current_level.player.dices = current_level.player.max_dices
        is_player_turn = False

    pygame.display.flip()
    timer.tick(fps)

pygame.quit()
