import pygame
import objects


class Level:
    def __init__(self, name, player, enemy, background, images, music):
        self.name = name
        self.name_text = objects.Text(name, pygame.color.Color("BLUE"), 640, 60)
        self.player = player
        self.enemy = enemy
        self.background = background
        self.set_of_dices = pygame.sprite.Group()
        self.set_of_cards = player.set_of_cards
        self.next_turn_button = objects.Button([images["BUTTON1"], images["BUTTON2"]], 1100, 60, "Next Turn")
        self.next_level = None
        self.music = music

    def update(self):
        self.set_of_dices.update()
        self.set_of_cards.update()
        self.next_turn_button.update()

        if self.next_turn_button.activated:
            self.next_turn_button.activated = False
            return 'nt'

    def draw(self, surface, is_player_turn):
        surface.blit(self.background, (0, 0))
        self.next_turn_button.draw(surface)

        self.enemy.draw(surface)
        self.player.draw(surface)

        if is_player_turn:
            self.set_of_cards.draw(surface)
        self.set_of_dices.draw(surface)
        self.name_text.draw(surface)


class Menu:
    def __init__(self, background, images, first_button_text, player, enemy, music):
        self.background = background
        self.start_button = objects.Button([images["BUTTON1"], images["BUTTON2"]], 640, 200, first_button_text)
        self.quit_button = objects.Button([images["BUTTON1"], images["BUTTON2"]], 640, 400, "Quit")
        self.set_of_cards = pygame.sprite.Group()
        self.set_of_dices = pygame.sprite.Group()
        self.player = player
        self.enemy = enemy
        self.music = music

    def update(self):
        self.start_button.update()
        self.quit_button.update()
        if self.start_button.activated:
            self.start_button.activated = False
            return 'b1'
        if self.quit_button.activated:
            self.quit_button.activated = False
            return 'bq'

    def draw(self, surface, a):
        surface.blit(self.background, (0, 0))
        self.start_button.draw(surface)
        self.quit_button.draw(surface)

