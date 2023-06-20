import pygame


class DiceCard(pygame.sprite.Sprite):
    def __init__(self, images, cx, cy, fighter, dmg, heal, roll=False, max_value=6):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # self.cx = cx
        # self.cy = cy
        self.rect.center = cx, cy
        self.fighter = fighter
        self.dmg = dmg
        self.heal = heal
        self.max_value = max_value
        self.roll = roll

    def action(self, target, damage, heal):
        # damage
        if damage * self.dmg > 0:
            self.fighter.action = 1
            self.fighter.frame_index = 0
            target.life -= damage * self.dmg
        # healing
        if heal * self.heal + self.fighter.life >= self.fighter.max_life:
            self.fighter.life = self.fighter.max_life
        else:
            self.fighter.life += heal * self.heal
        return self.roll, self.dmg * damage

    def draw(self, surface):
        surface.blit(self.image, self.rect)
