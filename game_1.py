import pygame, os, objects, random

#import Levels
import cards

pygame.init()

WIDTH = 1280
HEIGHT = 720
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

CLICKED_DICES = 0

running = True


class Level:
    def __init__(self, player, enemy, background):
        self.player = player
        self.enemy = enemy
        self.background = background
        self.set_of_dices = pygame.sprite.Group()
        self.set_of_cards = pygame.sprite.Group()

    def update(self):
        self.set_of_dices.update()
        self.set_of_cards.update()

        for d in self.set_of_dices:
            for c in self.set_of_cards:
                if d.rect.colliderect(c.rect) and not d.clicked and c.image == c.images[0]:
                    c.action(self.enemy, d.value + 1, 0, 0)
                    d.kill()
                    c.image = c.images[1]

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        self.enemy.draw(surface)
        self.player.draw(surface)

        self.set_of_cards.draw(surface)
        self.set_of_dices.draw(surface)


class Menu:
    def __init__(self, background, images):
        self.background = background
        self.start_button = objects.Button([images["BUTTON1"], images["BUTTON2"]], 640, 200, "Start")
        self.quit_button = objects.Button([images["BUTTON1"], images["BUTTON2"]], 640, 400, "Quit")

    def update(self):
        self.start_button.update()
        self.quit_button.update()
        if self.start_button.activated:
            global current_level
            current_level = l1
            self.start_button.activated = False
        if self.quit_button.activated:
            global running
            running = False
            self.quit_button.activated = False

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.start_button.draw(surface)
        self.quit_button.draw(surface)





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

DICES = [IMAGES["DICE1"], IMAGES["DICE2"], IMAGES["DICE3"], IMAGES["DICE4"], IMAGES["DICE5"], IMAGES["DICE6"], ]


enemy = objects.Fighter([IMAGES["ENEMY1"], IMAGES["ENEMY2"]], WIDTH - 80, 100)
player = objects.Fighter([IMAGES["PLAYER1"], IMAGES["PLAYER2"]], 80, HEIGHT - 100)

l1 = Level(player, enemy, BACKGROUND)
menu = Menu(BACKGROUND, IMAGES)


dice_spawn_x = 300
dice_spawn_y = HEIGHT + 70


current_level = l1
player.level = current_level
enemy.level = current_level

attack_card = cards.DiceCard([IMAGES["KARTA1"], IMAGES["KARTA1GRAY"]], 250, 300, player)
current_level.set_of_cards.add(attack_card)
attack_card.level = current_level

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current_level = menu
            elif event.key == pygame.K_SPACE:
                if player.dices > 0:
                    d = objects.Dice(DICES, dice_spawn_x, dice_spawn_y, random.randint(0, 5))
                    current_level.set_of_dices.add(d)
                    dice_spawn_x += 100
                    player.dices -= 1
            elif event.key == pygame.K_DOWN:
                enemy.life -= 1

    key_pressed = pygame.event.get()

    current_level.update()
    current_level.draw(screen)

    pygame.display.flip()
    timer.tick(fps)

pygame.quit()
