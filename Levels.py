import pygame


import objects


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
        self.start_button = objects.Button([images["BUTTON1"],images["BUTTON2"]], 640, 200, "RESUME")
        self.quit_button = objects.Button([images["BUTTON1"],images["BUTTON2"]], 640, 400, "QUIT")

    def update(self):
        self.start_button.update()
        self.quit_button.update()
        if self.start_button.activated:
            game_1.current_level = game_1.l1
        if self.quit_button.activated:
            game_1.running = False
    
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.start_button.draw(surface)
        self.quit_button.draw(surface)
