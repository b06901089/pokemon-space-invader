import pygame
import random
import config.constant as C

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, health, speed, fig, moves):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(C.BOSS_PATH[fig][0])
        self.image = pygame.transform.scale(img, C.BOSS_PATH[fig][1])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health_start = health
        self.health_remaining = self.health_start
        self.boss_speed = speed
        self.y_limit = C.SCREEN_HEIGHT // 2 - random.randint(0, 200)
        self.last_shot = 0
        self.shot_counter = 0
        self.moves = moves

    def draw_healthbar(self, surface):
        pygame.draw.rect(surface, C.RED, (self.rect.x, self.rect.bottom + 5, self.rect.width, 5))
        if self.health_remaining > 0:
            pygame.draw.rect(surface, C.GREEN, (self.rect.x, self.rect.bottom + 5, int(self.rect.width * (self.health_remaining / self.health_start)), 5))

    def update(self):
        if self.rect.bottom <= self.y_limit:
            self.rect.y += self.boss_speed
        else:
            if self.rect.left < 0:
                self.rect.left = 0
                self.boss_speed *= -1
            elif self.rect.right > C.SCREEN_WIDTH:
                self.rect.right = C.SCREEN_WIDTH
                self.boss_speed *= -1
            self.rect.x += self.boss_speed