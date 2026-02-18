# Sprite references:
# https://witpop.itch.io/sprite-pack-hred-envelope-icons

import pygame
import config.constant as C

class Hong_bao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/Red Envelope Starter Pack/Hong Bao S7.png")
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += 4
        if self.rect.top > C.SCREEN_HEIGHT:
            self.kill()