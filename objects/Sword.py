import pygame
import math
import config.constant as C

class Sword(pygame.sprite.Sprite):
    def __init__(self, spaceship, angle=0.0):
        pygame.sprite.Sprite.__init__(self)
        self.spaceship = spaceship
        img = pygame.image.load("img/sword.png")
        img = pygame.transform.scale(img, (32, 32))
        self.image = pygame.transform.rotate(img, 45)
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.centerx = self.spaceship.rect.centerx + C.SWORD_RANGE * math.cos(self.angle)
        self.rect.centery = self.spaceship.rect.centery + C.SWORD_RANGE * math.sin(self.angle)
    
    def update(self):
        self.angle += math.pi / 120.0
        self.rect.centerx = self.spaceship.rect.centerx + C.SWORD_RANGE * math.cos(self.angle)
        self.rect.centery = self.spaceship.rect.centery + C.SWORD_RANGE * math.sin(self.angle)
