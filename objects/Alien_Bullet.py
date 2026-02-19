import pygame
import config.constant as C

class Alien_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mode=0, bu_type=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(C.ALIEN_BULLET_PATH[bu_type])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.posX = float(self.rect.x)
        self.bullet_dir = C.ALIEN_BULLET_X_SPEED[mode]

    def update(self):
        self.posX -= self.bullet_dir
        self.rect.x = int(self.posX)
        self.rect.y += 2

        if self.rect.top > C.SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > C.SCREEN_WIDTH:
            self.kill()