"""
MOVES.JSON KEY USAGE DOCUMENTATION
==================================

The Animation class loads animation settings from config/moves.json.
Each move in the "moves" section is an array of animation configurations.
Below is a complete reference for all keys used in move configurations:

ANIMATION SETTING KEYS:
    - animation (str):
		Name of the animation defined in the "animations" section of moves.json.
		References which sprite animation frames to use.
		Default: Required field, no default.
    
    - speed (int, optional):
		Frame rate control. Number of update cycles before frame advances.
		Special value: -1 means static/non-animated (ex: bullets).
		Default: -1
    
    - repeat (int, optional):
		Number of times to loop through all animation frames.
		Default: 1
    
    - vx (float):
		Horizontal velocity. Pixel movement per update in x-direction.
		Can be negative for leftward movement.
		Default: Required field, no default.
    
    - vy (float):
		Vertical velocity. Pixel movement per update in y-direction.
		Direction can be inverted based on spawn_ops parameter.
		Default: Required field, no default.
    
    - offset_x (int, optional):
		Horizontal offset from spawn position for initial placement.
		Default: 0
    
    - offset_y (int, optional):
		Vertical offset from spawn position for initial placement.
		Default: 0
    
    - in_game_scaling (int, optional):
		Scale factor for the animation sprite during rendering.
		Multiplies sprite dimensions by this factor.
		Default: 1
    
    - power (int):
		Damage/effect value of the animation. Used for collision/damage calculations.
		Default: Required field, no default.
    
    - replicas (int, optional):
		Number of additional copies of this animation to spawn.
		0 means spawn only the primary animation.
		Default: 0
    
    - replica_delay (int, optional):
		Frame delay between spawning each replica in the sequence.
		Default: 0
    
    - move_direction (int, optional):
		Movement pattern type.
		0 or absent: Linear movement using vx/vy.
		1: Circular rotation around center point.
		Default: 0
    
    - starting_angle (float, optional):
		Initial angle in degrees for circular movement (move_direction=1).
		Converted to radians internally.
		Default: Only used when move_direction=1, no default value.
    
    - rotate_radius (int, optional):
		Distance from rotation center point for circular movement.
		Defines the orbit radius when move_direction=1.
		Default: Only used when move_direction=1, no default value.
"""

import pygame
import math
import config.constant as C

class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, ani, index, spawn_ops):
        pygame.sprite.Sprite.__init__(self)
        move_json = C.MOVE_JSON

        # Extrct datas and paths
        setting = move_json['moves'][ani][index]
        ani_part_name = setting['animation']
        data = move_json['animations'][ani_part_name]
        sheet_path = move_json['sprite'][data['sprite_sheet']]['url']
        

        # Optional keys
        self.speed = -1
        if 'speed' in setting:
            self.speed = setting['speed']
        self.repeat = 1
        if 'repeat' in setting:
            self.repeat = setting['repeat']
        self.in_game_scaling = 1
        if 'in_game_scaling' in setting:
            self.in_game_scaling = setting['in_game_scaling']
        self.move_dir = 0
        if 'move_direction' in setting:
            self.move_dir = setting['move_direction']
        self.offset_x = 0
        if 'offset_x' in setting:
            self.offset_x = setting['offset_x']
        self.offset_y = 0
        if 'offset_y' in setting:
            self.offset_y = setting['offset_y']


        # Load the spritesheet and extract the frames
        spritesheet = pygame.image.load(sheet_path).convert_alpha()
        self.images = []
        for num in range(data['frame_counts']):
            sprite = pygame.Surface((data['w'], data['h']), pygame.SRCALPHA)
            if data['horizontal_or_vertical'] == 0: # horizontal
                sprite.blit(spritesheet, (0, 0), pygame.Rect(data['x'] + data['w'] * num, data['y'], data['w'], data['h']))
            else:
                sprite.blit(spritesheet, (0, 0), pygame.Rect(data['x'], data['y'] + data['h'] * num, data['w'], data['h']))
            sprite = pygame.transform.scale(sprite, (data['w'] * self.in_game_scaling, data['h'] * self.in_game_scaling))
            self.images.append(sprite)

        # Basics
        self.counter = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x + self.offset_x, y + self.offset_y)
        self.pos = [x + self.offset_x, y + self.offset_y]

        # Store velocity settings
        self.vx = setting['vx']
        self.vy = setting['vy'] if not spawn_ops else -setting['vy']
        
        # Store direction settings
        if self.move_dir == 1:
            self.angle = setting['starting_angle'] * math.pi / 180.0
            self.rotate_radius = setting['rotate_radius']
            self.rotate_center = [x + self.offset_x, y + self.offset_y]
            self.rotate_pos = [x + self.offset_x, y + self.offset_y]

        # power settings
        self.power = setting['power']
        
    def update(self):

        # rotate around the center if move_dir is 1 (counter-clockwise)
        if self.move_dir == 1:
            self.rotate_center[0] += self.vx
            self.rotate_center[1] += self.vy
            self.angle += math.pi / 30.0
            self.rect.x = self.rotate_center[0] + self.rotate_radius * math.cos(self.angle)
            self.rect.y = self.rotate_center[1] + self.rotate_radius * math.sin(self.angle)
        else:
            self.pos[0] += self.vx
            self.pos[1] += self.vy
            self.rect.x = int(self.pos[0])
            self.rect.y = int(self.pos[1])

        # static objects
        if self.speed == -1:
            if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > C.SCREEN_WIDTH:
                self.kill()
            return

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