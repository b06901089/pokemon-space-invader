import pygame
import config.constant as C

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, pu_type):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(C.POWERUP_PATH[pu_type][0])
        self.image = pygame.transform.scale(img, C.POWERUP_PATH[pu_type][1])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pu_type = pu_type

    def update(self):
        powerup_speed = 4
        self.rect.y += powerup_speed
        
        if self.rect.top > C.SCREEN_HEIGHT:
            self.kill()