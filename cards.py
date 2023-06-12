import pygame


class DiceCard(pygame.sprite.Sprite):
    def __init__(self, images, cx, cy, fighter):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.cx = cx
        self.cy = cy
        self.rect.center = cx, cy
        self.active = True
        self.level = None
        self.fighter = fighter

    def action(self, target, damage, poison, heal):
        target.life -= damage
        target.poison += poison
        self.fighter.life += heal

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# class OneDiceCard(DiceCard):
#     def __init__(self, image, cx, cy, fighter):
#         super().__init__(image, cx, cy, fighter)
#
#
# class Attack(DiceCard):
#     def __init__(self, image, cx, cy, fighter):
#         super().__init__(image, cx, cy, fighter)
#
#     def action(self, target, damage):
#         super().action(target, damage, 0, 0)
#
#
# class CountingDiceCard(DiceCard):
#     def __init__(self, image, cx, cy, fighter, count):
#         super().__init__(image, cx, cy, fighter)
#         self.starting_count = count
#         self.count = self.starting_count

