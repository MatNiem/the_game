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

pygame.display.set_caption("Kościany loch")

CLICKED_DICES = 0

dice_spawn_x = 400
dice_spawn_y = HEIGHT + 70

running = True

# Wczytywanie obrazków
path = 'images'
file_names = sorted(os.listdir(path))
BACKGROUND_MENU = pygame.transform.scale_by(pygame.image.load(os.path.join(path, 'background_m.png')).convert(), 0.8)
BACKGROUND_2 = pygame.image.load(os.path.join(path, 'background.png')).convert()
BACKGROUND_1 = pygame.transform.scale_by(pygame.image.load(os.path.join(path, 'background2.jpg')).convert(), 2.5)
BACKGROUND_3 = pygame.transform.scale_by(pygame.image.load(os.path.join(path, 'background3.jpg')).convert(), 2.5)
N_LEVEL_SCREEN = pygame.image.load(os.path.join(path, 'n_level.jpg')).convert()
U_DIED_SCREEN = pygame.image.load(os.path.join(path, 'u_died.jpg')).convert()
W_GAME_SCREEN = pygame.image.load(os.path.join(path, 'w_game.jpg')).convert()
IMAGES = {}
for file_name in file_names:
    IMAGES[file_name[:-4].upper()] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND_1)

# wczytywanie dźwięków
sword_sound = pygame.mixer.Sound("sword_swing.mp3")
win_sound = pygame.mixer.Sound("win.mp3")
next_level_sound = pygame.mixer.Sound("next_level.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")

set_of_dices = pygame.sprite.Group()
set_of_cards = pygame.sprite.Group()

# tworzenie list sprite-ów

# dices
DICES = [IMAGES["DICE1"], IMAGES["DICE2"], IMAGES["DICE3"],
         IMAGES["DICE4"], IMAGES["DICE5"], IMAGES["DICE6"]]

# player animations
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
# enemy animations
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
# boss animations
BOSS_IDLE = [pygame.transform.scale_by(IMAGES["BOSS1"], 5),
             pygame.transform.scale_by(IMAGES["BOSS2"], 5),
             pygame.transform.scale_by(IMAGES["BOSS3"], 5),
             pygame.transform.scale_by(IMAGES["BOSS4"], 5), ]

BOSS_ATTACK = [pygame.transform.scale_by(IMAGES["BOSSA1"], 5),
               pygame.transform.scale_by(IMAGES["BOSSA2"], 5),
               pygame.transform.scale_by(IMAGES["BOSSA3"], 5),
               pygame.transform.scale_by(IMAGES["BOSSA4"], 5),
               pygame.transform.scale_by(IMAGES["BOSSA5"], 5),
               pygame.transform.scale_by(IMAGES["BOSSA6"], 5),
               pygame.transform.scale_by(IMAGES["BOSSA7"], 5),
               pygame.transform.scale_by(IMAGES["BOSSA8"], 5)]

BOSS_DEATH = [pygame.transform.scale_by(IMAGES["BOSSD1"], 5),
              pygame.transform.scale_by(IMAGES["BOSSD2"], 5),
              pygame.transform.scale_by(IMAGES["BOSSD3"], 5),
              pygame.transform.scale_by(IMAGES["BOSSD4"], 5),
              pygame.transform.scale_by(IMAGES["BOSSD5"], 5),
              pygame.transform.scale_by(IMAGES["BOSSD6"], 5),
              pygame.transform.scale_by(IMAGES["BOSSD7"], 5),
              pygame.transform.scale_by(IMAGES["BOSSD8"], 5),
              pygame.transform.scale_by(IMAGES["BOSSD9"], 5)]

# creating enemy objects
enemy = objects.Fighter("E0", ENEMY_IDLE, ENEMY_ATTACK, ENEMY_DEATH, WIDTH - 200, HEIGHT - 200)
enemy1 = objects.Fighter("E1", ENEMY_IDLE, ENEMY_ATTACK, ENEMY_DEATH, WIDTH - 200, HEIGHT - 200, dices=1)
enemy2 = objects.Fighter("E2", ENEMY_IDLE, ENEMY_ATTACK, ENEMY_DEATH, WIDTH - 200, HEIGHT - 200, dices=2)
enemy3 = objects.Fighter("E3", BOSS_IDLE, BOSS_ATTACK, BOSS_DEATH, WIDTH - 200, HEIGHT - 200, life=36, dices=3)

# creating player object
player = objects.Fighter("Player", PLAYER_IDLE, PLAYER_ATTACK, PLAYER_DEATH, 200, HEIGHT - 200, life=12, dices=2)

# Menu start:
m_start = Levels.Menu(BACKGROUND_MENU, IMAGES, "Start", player, enemy, "music_menu.mp3")
# Menu pause:
m_pause = Levels.Menu(BACKGROUND_MENU, IMAGES, "Continue", player, enemy, "music_menu.mp3")
# Poziom pierwszy:
l_one = Levels.Level("Level 1", player, enemy1, BACKGROUND_1, IMAGES, "music_level_one.mp3")
# Poziom drugi:
l_two = Levels.Level("Level 2", player, enemy2, BACKGROUND_2, IMAGES, "music_level_two.mp3")
# Poziom trzeci:
l_three = Levels.Level("Level 3", player, enemy3, BACKGROUND_3, IMAGES, "music_level_three.mp3")

# setting level values
l_one.next_level = l_two
l_two.next_level = l_three
l_three.next_level = m_start

current_level = m_start
last_level = l_one

# playing first music track
pygame.mixer.music.load(current_level.music)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

# Card objects
attack_card = cards.DiceCard([pygame.transform.scale_by(IMAGES["A1"], 0.35),
                              pygame.transform.scale_by(IMAGES["A1_BW"], 0.35)], 250, 300, player, 1, 0)
attack_card2 = cards.DiceCard([pygame.transform.scale_by(IMAGES["A2"], 0.35),
                               pygame.transform.scale_by(IMAGES["A2_BW"], 0.35)], 250, 300, player, 2, 0)
heal_card = cards.DiceCard([pygame.transform.scale_by(IMAGES["B1"], 0.35),
                            pygame.transform.scale_by(IMAGES["B1_BW"], 0.35)], 550, 300, player, 0, 1, max_value=4)
roll_card = cards.DiceCard([pygame.transform.scale_by(IMAGES["C1"], 0.35),
                            pygame.transform.scale_by(IMAGES["C1_BW"], 0.35)], 850, 300, player, 0, 0, True)

# adding cards to player's set
player.set_of_cards.add(attack_card)
player.set_of_cards.add(heal_card)
player.set_of_cards.add(roll_card)

# setting boolean values
is_player_turn = True
dices_spawned = False
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
                if current_level != m_start:
                    current_level, last_level = m_pause, current_level
            elif event.key == pygame.K_SPACE:
                spawn_dices(player, dice_spawn_x)

    # drawing level
    current_level.draw(screen, is_player_turn)

    # turn handling
    if not (current_level == m_pause or current_level == m_pause):
        # Player is dead:
        if player.life <= 0:
            current_level.player.action = 2
            if len(current_level.player.images_d) - 1 != current_level.player.frame_index \
                    and current_level.player.action == 2:
                pass
            else:
                pygame.time.wait(1000)
                screen.blit(U_DIED_SCREEN, (0, 0))
                pygame.display.flip()
                pygame.mixer.music.unload()
                game_over_sound.play()
                pygame.time.wait(3000)
                current_level, last_level = m_start, current_level
                pygame.mixer.music.load(current_level.music)
                pygame.mixer.music.play(-1)
                player.life = 1
        # Enemy is dead:
        elif current_level.enemy.life <= 0:
            current_level.enemy.action = 2
            if len(current_level.enemy.images_d) - 1 != current_level.enemy.frame_index \
                    and current_level.enemy.action == 2:
                pass
            else:
                pygame.mixer.music.unload()
                if current_level != l_three:
                    screen.blit(N_LEVEL_SCREEN, (0, 0))
                    next_level_sound.play()
                else:
                    screen.blit(W_GAME_SCREEN, (0, 0))
                    win_sound.play()
                pygame.display.flip()
                pygame.time.wait(2500)

                current_level, last_level = current_level.next_level, current_level
                pygame.mixer.music.load(current_level.music)
                pygame.mixer.music.play(-1)
                current_level.player.max_dices += 1
                current_level.player.dices = current_level.player.max_dices
                current_level.player.max_life += 6
                current_level.player.life += 6
                current_level.player.action = 0
                if current_level == l_three:
                    player.set_of_cards.remove(attack_card)
                    player.set_of_cards.add(attack_card2)
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
                            is_player_turn = True
                            sword_sound.play()
                        dices_spawned = False
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
                            result = c.action(current_level.enemy, d.value + 1, d.value + 1)
                            if result[0]:
                                dices_spawned = False
                                current_level.player.dices += 1
                            if result[1]:
                                sword_sound.play()
                            d.kill()
                            c.image = c.images[1]

    # handling buttons
    option = current_level.update()
    if option == 'b1':  # start / continue button
        pygame.mixer.music.unload()
        current_level, last_level = last_level, current_level
        pygame.mixer.music.load(current_level.music)
        pygame.mixer.music.play(-1)
        if last_level == m_start:
            # reseting statistics
            current_level = l_one
            player.max_dices = 2
            current_level.player.dices = current_level.player.max_dices
            spawn_dices(current_level.player, dice_spawn_x)
            l_one.enemy.life = l_one.enemy.max_life
            l_two.enemy.life = l_two.enemy.max_life
            l_three.enemy.life = l_three.enemy.max_life
            player.set_of_cards.empty()
            player.set_of_cards.add(attack_card)
            player.set_of_cards.add(heal_card)
            player.set_of_cards.add(roll_card)
            for c in player.set_of_cards:
                c.image = c.images[0]
            player.max_life = 12
            player.life = player.max_life
    elif option == 'bq':  # quit button
        running = False
    elif option == 'nt' and is_player_turn:  # next level button
        for dice in current_level.set_of_dices:
            dice.kill()
        for card in current_level.set_of_cards:
            card.image = card.images[0]
        current_level.player.dices = current_level.player.max_dices
        is_player_turn = False

    pygame.display.flip()
    timer.tick(fps)

pygame.quit()
