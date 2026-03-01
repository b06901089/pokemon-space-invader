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

STARTING_PHASE = 1 # modify this to test different phases directly
MAX_PHASE = 7

ORG_ALIEN_PATH = [
    'img/org_space_invader/alien1.png',
    'img/org_space_invader/alien2.png',
    'img/org_space_invader/alien3.png',
    'img/org_space_invader/alien4.png',
    'img/org_space_invader/alien5.png',
]
SPAWN_ALIEN_COOLDOWN = 180 # spawn a new alien every {#} frames at the beginning
SPAWN_ALIEN_COOLDOWN_MIN = 10
SPAWN_ALIEN_COOLDOWN_DECREASE = 5
SPAWN_ALIEN_REPEAT = 4

BOSS_PATH = {
    # 2: ['img/edited/boss1.png', (160, 160)],
    # 3: ['img/edited/boss2.png', (60, 45)],
    'gen3_fearow': ['img/pokemon/gen3/fearow.png', (56, 56)],
    'gen3_torchic': ['img/pokemon/gen3/torchic.png', (64, 64)],
    'gen3_mankey': ['img/pokemon/gen3/mankey.png', (64, 64)],
    'gen5_exeggutor': ['img/pokemon/gen5/exeggutor.png', (96, 96)],
    'gen5_altaria': ['img/pokemon/gen5/altaria.png', (96, 96)],
    'gen5_zapdos': ['img/pokemon/gen5/zapdos.png', (120, 120)],
}


POWERUP_SPAWN_TIME = 400 # spawn the first powerup at the {#} frames
POWERUP_RECOVER_HEALTH = 3

SWORD_RANGE = 250

HONG_BAO_SPAWN_TIME = 400 # spawn the first hong bao at the {#} frames

POWERUP_PATH = [
    (-1, (-1, -1)),
    ('img/Free - Raven Fantasy Icons/64x64/fc51.png', (48, 48)),
    ('img/powerup/HH_face_1.png', (64, 64)),
    ('img/Free - Raven Fantasy Icons/64x64/fc759.png', (32, 32)),
    ('img/Free - Raven Fantasy Icons/64x64/fc155.png', (32, 32)),
]
SWORD_PATH = 'img/edited/sword.png'

# SPAWN_ALIENS_TEAMS_COOLDOWN = 7200
# SPAWN_ALIENS_TEAMS_MAP = [
#     [-50, 100, 2, 5, '#0043', True],
#     [-50, -50, 2, 5, '#0043', True],
#     [-50, -200, 2, 5, '#0043', True],
#     [SCREEN_WIDTH + 50, 100, -2, 5, '#0043', False],
#     [SCREEN_WIDTH + 50, -50, -2, 5, '#0043', False],
#     [SCREEN_WIDTH + 50, -200, -2, 5, '#0043', False],

#     [-50, 100, 2, 4, '#0043', True],
#     [-50, -50, 2, 4, '#0043', True],
#     [-50, -200, 2, 4, '#0043', True],
#     [SCREEN_WIDTH + 50, 100, -2, 4, '#0043', False],
#     [SCREEN_WIDTH + 50, -50, -2, 4, '#0043', False],
#     [SCREEN_WIDTH + 50, -200, -2, 4, '#0043', False],

#     [-50, 300, 2, 3, '#0043', True],
#     [-50, 150, 2, 3, '#0043', True],
#     [-50, 0, 2, 3, '#0043', True],
#     [SCREEN_WIDTH + 50, 300, -2, 3, '#0043', False],
#     [SCREEN_WIDTH + 50, 150, -2, 3, '#0043', False],
#     [SCREEN_WIDTH + 50, 0, -2, 3, '#0043', False],

#     [-50, SCREEN_HEIGHT - 200, 4, 0, '#0043', True],
#     [-50, SCREEN_HEIGHT - 400, 4, 0, '#0043', True],
#     [SCREEN_WIDTH + 50, SCREEN_HEIGHT - 200, -4, 0, '#0043', False],
#     [SCREEN_WIDTH + 50, SCREEN_HEIGHT - 400, -4, 0, '#0043', False],
# ]

# Animation reference
# https://www.youtube.com/watch?v=mnCPCgA3HvI
# the video is arranged roughly according to aphabetical order
# gust 13:42
# whirlwind 26:11
# sacred fire 28:26
# bite 29:28
# surf 29:54
# shadow ball 30:13
# shock wave 30:36
# sky attack 31:40
# slash 32:00
# steel wing 34:25
# thunder (series) 37:30

MOVE_JSON_PATH = 'config/moves.json'
with open(MOVE_JSON_PATH, 'r') as f:
    MOVE_JSON = json.load(f)

ITEM_JSON_PATH = 'config/items.json'
with open(ITEM_JSON_PATH, 'r') as f:
    ITEM_JSON = json.load(f)

ITEM_WEIGHTS = [ITEM_JSON[item]['weight'] for item in ITEM_JSON]

INVENTORY_SHOW_KEY = ['q', 'w', 'e', 'a', 's', 'd']

ENEMY_JSON_PATH = 'config/enemy.json'
with open(ENEMY_JSON_PATH, 'r') as f:
    ENEMY_JSON = json.load(f)
ENEMY_JSON_KEYS = list(ENEMY_JSON.keys())

POKE_JSON_PATH = 'config/poke.json'
with open(POKE_JSON_PATH, 'r') as f:
    POKE_JSON = json.load(f)

PRE_MOVE_PATH = 'config/pre_moves.json'
with open(PRE_MOVE_PATH, 'r') as f:
    PRE_MOVE_JSON = json.load(f)