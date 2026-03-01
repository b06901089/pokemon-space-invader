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
    
    - rotate (float, optional):
        Rotation of the sprite. Positive numbers indicate counter-clock wise.
        Default: 0

    - vx (float, optional):
		Horizontal velocity. Pixel movement per update in x-direction.
		Can be negative for leftward movement.
		Default: Required field, no default.
        Default: 0
    
    - vy (float, optional):
		Vertical velocity. Pixel movement per update in y-direction.
		Direction can be inverted based on spawn_ops parameter.
		Default: Required field, no default.
        Default: 0
    
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

    - spawn_reset (bool, optional):
        Does the replicas' spawn locations reset with each replica.
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

    - pre_move (string, optional):
        Define the movement of Boss or Attacker before starting the attack animation. 
        The movement is meant to used as a hint before attacking.
        Default: None

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
        self.rotate = 0
        if 'rotate' in setting:
            self.rotate = setting['rotate']
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
        self.vx = 0
        if 'vx' in setting:
            self.vx = setting['vx']
        self.vy = 0
        if 'vy' in setting:
            self.vy = setting['vy'] if not spawn_ops else -setting['vy']
        self.pre_move = None
        self.time_delay = 0
        if 'pre_move' in setting:
            self.pre_move, self.time_delay = self.parse_pre_move(C.PRE_MOVE_JSON[setting['pre_move']])

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
            if self.rotate != 0:
                sprite = pygame.transform.rotate(sprite, self.rotate)
            self.images.append(sprite)

        # Basics
        self.counter = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x + self.offset_x, y + self.offset_y)
        self.pos = [x + self.offset_x, y + self.offset_y]
        
        # Store direction settings
        if self.move_dir == 1:
            self.angle = setting['starting_angle'] * math.pi / 180.0
            self.rotate_radius = setting['rotate_radius']
            self.rotate_center = [x + self.offset_x, y + self.offset_y]
            self.rotate_pos = [x + self.offset_x, y + self.offset_y]

        # power settings
        self.power = setting['power']

        # don't delete before it appears for the first time
        self.appear = False
        
    def parse_pre_move(self, lst):
        if len(lst) % 3 != 0:
            raise ValueError("List length must be a multiple of 3")
        rows = [lst[i:i+3] for i in range(0, len(lst), 3)]
        last_sum = sum(row[-1] for row in rows)

        return rows, last_sum

    def update(self):

        if self.time_delay > 0:
            self.time_delay -= 1
            return

        # rotate around the center if move_dir is 1 (counter-clockwise)
        if self.move_dir == 1:
            self.rotate_center[0] += self.vx
            self.rotate_center[1] += self.vy
            self.angle += math.pi / 20.0
            self.rect.centerx = self.rotate_center[0] + self.rotate_radius * math.cos(self.angle)
            self.rect.centery = self.rotate_center[1] + self.rotate_radius * math.sin(self.angle)
        else:
            self.pos[0] += self.vx
            self.pos[1] += self.vy
            self.rect.centerx = int(self.pos[0])
            self.rect.centery = int(self.pos[1])

        # static objects
        if self.speed == -1:
            if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > C.SCREEN_WIDTH or self.rect.top > C.SCREEN_HEIGHT:
                if self.appear:
                    self.kill()
            else:
                self.appear = True
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