import pygame

CLICKED_DICE = 0
ID = 0


class Dice(pygame.sprite.Sprite):
    def __init__(self, images, cx, cy, value):
        super().__init__()
        self.images = images
        self.image = self.images[value]
        self.rect = self.image.get_rect()
        self.cx = cx
        self.cy = cy
        self.rect.center = cx, cy
        self.speed = 80
        self.clicked = False
        self.level = None
        self.value = value
        global ID
        ID += 1
        self.id = ID

    def _get_event(self):
        pos = pygame.mouse.get_pos()

        global CLICKED_DICE
        # przesuwanie kości
        if pygame.mouse.get_pressed()[0] and (CLICKED_DICE == 0 or CLICKED_DICE == self.id):
            if self.rect.collidepoint(pos):
                self.clicked = True
                CLICKED_DICE = self.id
        elif pygame.mouse.get_pressed()[2]:
            if self.rect.collidepoint(pos):
                self.rect.center = self.cx, self.cy
        elif not pygame.mouse.get_pressed()[0]:
            self.clicked = False
            CLICKED_DICE = 0

        if self.clicked:
            self.rect.center = pos

    def update(self):
        self._get_event()
        # wysuwanie spod ekranu
        self.rect.y -= self.speed
        self.speed /= 2

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Text:
    def __init__(self, text, text_colour, pc_x, pc_y, font_type=None, font_size=36):
        self.text = str(text)
        self.text_colour = text_colour
        self.font_size = font_size
        self.font_type = font_type
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.image = self.font.render(self.text, True, self.text_colour)
        self.rect = self.image.get_rect()
        self.rect.center = pc_x, pc_y

    def draw(self, surface):
        self.image = self.font.render(self.text, True, self.text_colour)
        surface.blit(self.image, self.rect)


class Fighter(pygame.sprite.Sprite):
    def __init__(self, images, cx, cy, cards=None, life=10, dices=3):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self._count = 0
        self.rect = self.image.get_rect()
        self.cx = cx
        self.cy = cy
        self.rect.center = cx, cy
        self.life = life
        self.life_display = Text(life, 'red', cx, cy + 80)
        self.poison = 0
        self.level = None
        self.dices = dices
        if not cards:
            self.cards = cards

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self._move(self.images)
        self.life_display.text = str(self.life)
        self.life_display.draw(surface)

    def _move(self, image_list):
        self.image = image_list[self._count // 20]
        self.rect = self.image.get_rect()
        self.rect.center = self.cx, self.cy
        self._count = (self._count + 1) % 40


class Button(pygame.sprite.Sprite):
    def __init__(self, images, cx, cy, text):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.cx = cx
        self.cy = cy
        self.rect.center = cx, cy
        self.text = text
        self.generated_text = Text(text, pygame.color.Color("BLUE"), cx, cy)
        self.activated = False

    def button_action(self):
        self.activated = True

    def _get_event(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.images[1]
            if pygame.mouse.get_pressed()[0]:
                self.button_action()
        else:
            self.image = self.images[0]

    def update(self):
        self._get_event()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.generated_text.draw(surface)
