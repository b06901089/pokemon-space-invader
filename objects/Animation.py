import pygame
import math
import config.constant as C

class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, ani, index):
        pygame.sprite.Sprite.__init__(self)
        move_json = C.MOVE_JSON

        # Extrct datas and paths
        setting = move_json['moves'][ani][index]
        ani_part_name = setting['animation']
        data = move_json['animations'][ani_part_name]
        sheet_path = move_json['sprite'][data['sprite_sheet']]['url']
        
        # Load the spritesheet and extract the frames
        spritesheet = pygame.image.load(sheet_path).convert_alpha()
        self.images = []
        for num in range(data['frame_counts']):
            sprite = pygame.Surface((data['w'], data['h']), pygame.SRCALPHA)
            if data['horizontal_or_vertical'] == 0: # horizontal
                sprite.blit(spritesheet, (0, 0), pygame.Rect(data['x'] + data['w'] * num, data['y'], data['w'], data['h']))
            else:
                sprite.blit(spritesheet, (0, 0), pygame.Rect(data['x'], data['y'] + data['h'] * num, data['w'], data['h']))
            sprite = pygame.transform.scale(sprite, (data['w'] * setting['in_game_scaling'], data['h'] * setting['in_game_scaling']))
            self.images.append(sprite)

        # Basics
        self.counter = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Store animation settings
        self.speed = setting['speed']
        self.repeat = setting['repeat']
        self.vx = setting['vx']
        self.vy = setting['vy']
        self.move_dir = setting['move_direction']
        self.angle = setting['starting_angle'] * math.pi / 180.0
        self.rotate_radius = setting['rotate_radius']
        self.rotate_center = [x, y]
        
    def update(self):

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
        if self.counter >= self.speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        elif self.counter >= self.speed and self.index >= len(self.images) - 1 and self.repeat > 1:
            self.counter = 0
            self.index = 0
            self.image = self.images[self.index]
            self.repeat -= 1
        elif self.counter >= self.speed and self.index >= len(self.images) - 1 and self.repeat <= 1:
            self.kill()