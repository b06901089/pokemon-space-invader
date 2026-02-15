import pygame
import config.constant as C

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, pu_type):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f"img/pu{pu_type}.png")
        self.image = pygame.transform.scale(img, C.IMG_SCALING_MAP['pu_type'][pu_type])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pu_type = pu_type

    def update(self):
        powerup_speed = 4
        self.rect.y += powerup_speed
        
        if self.rect.top > C.SCREEN_HEIGHT:
            self.kill()