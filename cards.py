import pygame


class DiceCard(pygame.sprite.Sprite):
    def __init__(self, images, cx, cy, fighter, dmg, heal, roll=False, max_value=6):
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
        self.dmg = dmg
        self.heal = heal
        self.max_value = max_value
        self.roll = roll

    def action(self, target, damage, heal):
        if damage * self.dmg > 0:
            self.fighter.action = 1
            target.life -= damage * self.dmg
        if heal * self.heal + self.fighter.life >= self.fighter.max_life:
            self.fighter.life = self.fighter.max_life
        else:
            self.fighter.life += heal * self.heal
        return self.roll

    def draw(self, surface):
        surface.blit(self.image, self.rect)
