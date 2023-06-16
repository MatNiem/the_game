import pygame

CLICKED_DICE = 0
ID = 0

red = (255, 0, 0)
green = (0, 255, 0)


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


class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, surface, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, red, (self.x - 75, self.y, 150, 20))
        pygame.draw.rect(surface, green, (self.x - 75, self.y, 150 * ratio, 20))


class Fighter(pygame.sprite.Sprite):
    def __init__(self, name, images, images_a, cx, cy, life=12, dices=3):
        super().__init__()
        self.name = name
        self.images = images
        self.images_a = images_a
        self.image = self.images[0]
        self.image_a = self.images_a[0]
        self._count = 0
        self.rect = self.image.get_rect()
        self.cx = cx
        self.cy = cy
        self.rect.center = cx, cy
        self.max_life = life
        self.life = life
        self.life_bar = HealthBar(cx, cy + 160, self.life, self.max_life)
        self.poison = 0
        self.level = None
        self.max_dices = dices
        self.dices = self.max_dices
        self.set_of_cards = pygame.sprite.Group()

    def draw(self, surface, is_attacking):
        surface.blit(self.image, self.rect)
        if is_attacking:
            self._attack(self.images_a)
        else:
            self._move(self.images)
        self.life_bar.draw(surface, self.life)

    def _move(self, image_list):
        self.image = image_list[self._count // 20]
        self.rect = self.image.get_rect()
        self.rect.center = self.cx, self.cy
        self._count = (self._count + 1) % 40

    def _attack(self, image_list):
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
