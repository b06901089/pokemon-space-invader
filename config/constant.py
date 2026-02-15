GAME_TITLE = "Space Invaders"

DEFAULT_VOLUME = 0.02

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

SPACESHIP_HEALTH = 25
BULLET_COOLDOWN = 1000 # shoot every {#/1000} second at the start
BULLET_DIR = [0, 1, -1, 3, -3]

ALIEN_PATH = {
    '#0458': 'img/pokemon/mantyke_48.png'
}
ALIEN_SHOT_COOLDOWN = 2000 # shoot every {#/1000} second
ALIEN_SHOT_RATIO = 5 # one bulet every # aliens
ALIEN_UNBREAKABLE_SHOT_RATIO = 20 # one unbreakable bulet every # aliens
ALIEN_BULLET_DIR = [0, 0.25, -0.25]
SPAWN_ALIEN_COOLDOWN = 120 # spawn a new alien every {#} frames at the beginning
SPAWN_ALIEN_COOLDOWN_MIN = 10
SPAWN_ALIEN_COOLDOWN_DECREASE = 5
SPAWN_ALIEN_REPEAT = 2
PHASE_2_THRESHOLD = 5 # number of aliens to kill before phase 2 starts

BOSS_PATH = [
    'None_Path',
    'None_Path',
    'img/boss1.png',
    'img/boss2.png',
    'img/pokemon/exeggutor.png',
]
# BOSS_HEALTH = 5
# BOSS_MOVE_SPEED = 1
# BOSS_SHOT_COOLDOWN = 500 # shoot every {#/1000} second
# BOSS_REST_EVERY = 4 # rest every {#} shots
# BOSS_REST_TIME = 5000 # rest for {#/1000} seconds every time the boss shoots


POWERUP_SPAWN_TIME = 100 # spawn the first powerup at the {#} frames
POWERUP_RECOVER_HEALTH = 3
# POWERUP_DECREASE_COOLDOWN = 150
# POWERUP_COOLDOWN_MIN = 100
POWERUP_COOLDOWN_LIST = [0, 150, 300, 450, 550, 650, 750, 800, 850, 875, 900]
BULLET_MODE_DICT = {
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

IMG_SCALING_MAP = {
    'boss_fig': [(-1, -1), (-1, -1), (160, 160), (60, 45), (96, 96)],
    'pu_type': [(-1, -1), (48, 48), (64, 64), (32, 32), (32, 32)]
}

SPAWN_ALIENS_TEAMS_COOLDOWN = 7200
SPAWN_ALIENS_TEAMS_MAP = [
    [-50, 100, 2, 5, '#0458', True],
    [-50, -50, 2, 5, '#0458', True],
    [-50, -200, 2, 5, '#0458', True],
    [SCREEN_WIDTH + 50, 100, -2, 5, '#0458', False],
    [SCREEN_WIDTH + 50, -50, -2, 5, '#0458', False],
    [SCREEN_WIDTH + 50, -200, -2, 5, '#0458', False],

    [-50, 100, 2, 4, '#0458', True],
    [-50, -50, 2, 4, '#0458', True],
    [-50, -200, 2, 4, '#0458', True],
    [SCREEN_WIDTH + 50, 100, -2, 4, '#0458', False],
    [SCREEN_WIDTH + 50, -50, -2, 4, '#0458', False],
    [SCREEN_WIDTH + 50, -200, -2, 4, '#0458', False],

    [-50, 300, 2, 3, '#0458', True],
    [-50, 150, 2, 3, '#0458', True],
    [-50, 0, 2, 3, '#0458', True],
    [SCREEN_WIDTH + 50, 300, -2, 3, '#0458', False],
    [SCREEN_WIDTH + 50, 150, -2, 3, '#0458', False],
    [SCREEN_WIDTH + 50, 0, -2, 3, '#0458', False],

    [-50, SCREEN_HEIGHT - 200, 4, 0, '#0458', True],
    [-50, SCREEN_HEIGHT - 400, 4, 0, '#0458', True],
    [SCREEN_WIDTH + 50, SCREEN_HEIGHT - 200, -4, 0, '#0458', False],
    [SCREEN_WIDTH + 50, SCREEN_HEIGHT - 400, -4, 0, '#0458', False],
]