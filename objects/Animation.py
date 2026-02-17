import pygame
import config.constant as C

class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, ani, sheet):
        pygame.sprite.Sprite.__init__(self)
        spritesheet = pygame.image.load(C.Animation_sprite[sheet]).convert_alpha()
        data = C.ANIMATION_SPRTIES[ani]

        self.ani = ani
        self.images = []
        for num in range(data[5]):
            sprite = pygame.Surface((data[2], data[3]), pygame.SRCALPHA)
            if data[4]:
                sprite.blit(spritesheet, (0, 0), pygame.Rect(data[0] + data[2] * num, data[1], data[2], data[3]))
            else:
                sprite.blit(spritesheet, (0, 0), pygame.Rect(data[0], data[1] + data[3] * num, data[2], data[3]))
            sprite = pygame.transform.scale(sprite, (32, 32))
            self.images.append(sprite)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.repeat_set = data[6]
        self.vx = data[7]
        self.vy = data[8]

    def update(self):
        animation_speed = 10

        self.counter += 1
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.counter >= animation_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        elif self.counter >= animation_speed and self.index >= len(self.images) - 1 and self.repeat_set > 1:
            self.counter = 0
            self.index = 0
            self.image = self.images[self.index]
            self.repeat_set -= 1
        elif self.counter >= animation_speed and self.index >= len(self.images) - 1 and self.repeat_set <= 1:
            self.kill()