import math
import json

# Game general settings
GAME_TITLE = "Space Invaders"

DEFAULT_VOLUME = 0.02

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


# Game object setting
SPACESHIP_HEALTH = 25
BULLET_COOLDOWN = 1000 # shoot every {#/1000} second at the start
BULLET_X_SPEED = [0, 1, -1, 3, -3] # relative to fixed y speed


ALIEN_PATH = {
    '#0043': 'img/pokemon/gen3/oddish.png',
    '#0458': 'img/pokemon/gen4/mantyke_48.png'
}
ALIEN_SHOT_COOLDOWN = 2000 # shoot bullet every {#/1000} second
ALIEN_SHOT_RATIO = 5 # one bulet every # aliens
ALIEN_UNBREAKABLE_SHOT_RATIO = 20 # one unbreakable bulet every # aliens
ALIEN_BULLET_X_SPEED = [0, 0.25, -0.25]
SPAWN_ALIEN_COOLDOWN = 120 # spawn a new alien every {#} frames at the beginning
SPAWN_ALIEN_COOLDOWN_MIN = 10
SPAWN_ALIEN_COOLDOWN_DECREASE = 5
SPAWN_ALIEN_REPEAT = 2


BOSS_PATH = {
    # 2: ['img/boss1.png', (160, 160)],
    2: ['img/pokemon/gen2/fearow.png', (56, 56)],
    # 3: ['img/boss2.png', (60, 45)],
    3: ['img/pokemon/gen3/torchic.png', (64, 64)],
    4: ['img/pokemon/gen5/exeggutor.png', (96, 96)],
}


POWERUP_SPAWN_TIME = 200 # spawn the first powerup at the {#} frames
POWERUP_RECOVER_HEALTH = 3
# POWERUP_COOLDOWN_DECREASE = 150
# POWERUP_COOLDOWN_MIN = 100
POWERUP_BULLET_CD = [0, 150, 300, 450, 550, 650, 750, 800, 850, 875, 900]
POWERUP_FIRE_MODES = {
    1: [(0, 0)],
    2: [(-10, 0), (10, 0)],
    3: [(0, 0), (-20, 0), (20, 0)],
    4: [(-10, 0), (10, 0), (-30, 1), (30, 2)],
    5: [(0, 0), (-20, 1), (20, 2), (-40, 1), (40, 2)],
    6: [(0, 0), (-20, 0), (20, 0), (-40, 1), (40, 2), (-60, 3), (60, 4)],
}
SWORD_RANGE = 250
HONG_BAO_SPAWN_TIME = 400 # spawn the first hong bao at the {#} frames
# HONG_BAO_SPAWN_TIME_DECREASE = 60
# HONG_BAO_SPAWN_TIME_MIN = 60

POWERUP_PATH = [
    (-1, (-1, -1)),
    ('img/powerup/pu1.png', (48, 48)),
    ('img/powerup/pu2.png', (64, 64)),
    ('img/powerup/pu3.png', (32, 32)),
    ('img/powerup/pu4.png', (32, 32)),
]

SPAWN_ALIENS_TEAMS_COOLDOWN = 7200
SPAWN_ALIENS_TEAMS_MAP = [
    [-50, 100, 2, 5, '#0043', True],
    [-50, -50, 2, 5, '#0043', True],
    [-50, -200, 2, 5, '#0043', True],
    [SCREEN_WIDTH + 50, 100, -2, 5, '#0043', False],
    [SCREEN_WIDTH + 50, -50, -2, 5, '#0043', False],
    [SCREEN_WIDTH + 50, -200, -2, 5, '#0043', False],

    [-50, 100, 2, 4, '#0043', True],
    [-50, -50, 2, 4, '#0043', True],
    [-50, -200, 2, 4, '#0043', True],
    [SCREEN_WIDTH + 50, 100, -2, 4, '#0043', False],
    [SCREEN_WIDTH + 50, -50, -2, 4, '#0043', False],
    [SCREEN_WIDTH + 50, -200, -2, 4, '#0043', False],

    [-50, 300, 2, 3, '#0043', True],
    [-50, 150, 2, 3, '#0043', True],
    [-50, 0, 2, 3, '#0043', True],
    [SCREEN_WIDTH + 50, 300, -2, 3, '#0043', False],
    [SCREEN_WIDTH + 50, 150, -2, 3, '#0043', False],
    [SCREEN_WIDTH + 50, 0, -2, 3, '#0043', False],

    [-50, SCREEN_HEIGHT - 200, 4, 0, '#0043', True],
    [-50, SCREEN_HEIGHT - 400, 4, 0, '#0043', True],
    [SCREEN_WIDTH + 50, SCREEN_HEIGHT - 200, -4, 0, '#0043', False],
    [SCREEN_WIDTH + 50, SCREEN_HEIGHT - 400, -4, 0, '#0043', False],
]

# Animation reference
# https://www.youtube.com/watch?v=mnCPCgA3HvI
MOVE_JSON_PATH = 'config/moves.json'
with open(MOVE_JSON_PATH, 'r') as f:
    MOVE_JSON = json.load(f)