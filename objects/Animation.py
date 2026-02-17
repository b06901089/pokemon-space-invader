import pygame
import math
import config.constant as C

class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, ani, index):
        pygame.sprite.Sprite.__init__(self)
        spritesheet = pygame.image.load(C.ANIMATION_SPRTIES[sheet]).convert_alpha()
        data = C.ANIMATION_SPRTIES[ani][index]
        self.ani = ani
        self.images = []
        for num in range(data[5]):
            sprite = pygame.Surface((data[2], data[3]), pygame.SRCALPHA)
            if data[4]:
                sprite.blit(spritesheet, (0, 0), pygame.Rect(data[0] + data[2] * num, data[1], data[2], data[3]))
            else:
                sprite.blit(spritesheet, (0, 0), pygame.Rect(data[0], data[1] + data[3] * num, data[2], data[3]))
            sprite = pygame.transform.scale(sprite, (data[2] * data[9], data[3] * data[9]))
            self.images.append(sprite)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.repeat_set = data[6]
        self.vx = data[7]
        self.vy = data[8]
        self.move_dir = data[10]
        self.angle = data[11]
        self.rotate_radius = 16
        self.rotate_center = [x, y]

    def update(self):
        animation_speed = 10

        # rotate around the center if move_dir is 1 (counter-clockwise)
        if self.move_dir == 1:
            self.rotate_center[0] += self.vx
            self.rotate_center[1] += self.vy
            self.angle += math.pi / 30.0
            self.rect.x = self.rotate_center[0] + self.rotate_radius * math.cos(self.angle)
            self.rect.y = self.rotate_center[1] + self.rotate_radius * math.sin(self.angle)
        else:
            self.rect.x += self.vx
            self.rect.y += self.vy

        self.counter += 1
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