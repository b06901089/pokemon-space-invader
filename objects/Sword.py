import pygame
import math
import config.constant as C

class Sword(pygame.sprite.Sprite):
    def __init__(self, target, angle=0.0):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        img = pygame.image.load(C.SWORD_PATH)
        img = pygame.transform.scale(img, (32, 32))
        self.image = pygame.transform.rotate(img, 45)
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.centerx = self.target.rect.centerx + C.SWORD_RANGE * math.cos(self.angle)
        self.rect.centery = self.target.rect.centery + C.SWORD_RANGE * math.sin(self.angle)
    
    def update(self):
        self.angle += math.pi / 150.0
        self.rect.centerx = self.target.rect.centerx + C.SWORD_RANGE * math.cos(self.angle)
        self.rect.centery = self.target.rect.centery + C.SWORD_RANGE * math.sin(self.angle)
