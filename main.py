import pygame
import random
import math
import json

from objects import *
from config import sound_manager
from collisions import resolve_all
import config.constant as C


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)


sound_manager.load("explosion", "img/explosion.wav")
sound_manager.load("explosion2", "img/explosion2.wav")
sound_manager.load("laser", "img/laser.wav")


# define constants
powerup_spawn_time = C.POWERUP_SPAWN_TIME
spaceship_health = C.SPACESHIP_HEALTH
screen_width = C.SCREEN_WIDTH
screen_height = C.SCREEN_HEIGHT
game_title = C.GAME_TITLE
red = C.RED
green = C.GREEN
blue = C.BLUE
white = C.WHITE
spawn_alien_repeat = C.SPAWN_ALIEN_REPEAT
hong_bao_spawn_time = C.HONG_BAO_SPAWN_TIME
bullet_mode_dict = C.BULLET_MODE_DICT
bg_scroll_speed = 1  # pixels per frame;


# define other game variables
last_alien_shot = pygame.time.get_ticks()
last_boss_shot = pygame.time.get_ticks()
last_countdown = pygame.time.get_ticks()
last_alien_team = pygame.time.get_ticks()
countdown = 3
game_phase = 1
state = 0
killed_aliens = 0
game_over = 0 # 0 is game not over, 1 is player has won, -1 is player has lost
boss_shot_counter = 0
hong_bao_collected = 0
boss_wave_active = False


# define FPS
clock = pygame.time.Clock()
fps = 60


# create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(game_title)


# loading background image
background = pygame.image.load("img/bg.png")


# define font
font20 = pygame.font.SysFont("Constantia", 20)
font30 = pygame.font.SysFont("Constantia", 30)
font40 = pygame.font.SysFont("Constantia", 40)


# create sprites groups
sprite_groups = {
    'spaceship': pygame.sprite.Group(),
    'bullet': pygame.sprite.Group(),
    'alien': pygame.sprite.Group(),
    'alien_bullet': pygame.sprite.Group(),
    'unbreakable_bullet': pygame.sprite.Group(),
    'explosion': pygame.sprite.Group(),
    'powerup': pygame.sprite.Group(),
    'boss': pygame.sprite.Group(),
    'hong_bao': pygame.sprite.Group(),
    'sword': pygame.sprite.Group(),
}

# scrolling background variables
def draw_bg():
    """Scroll the background vertically to create a moving effect.

    This draws the background twice and advances a y-offset each frame so
    the image appears to loop continuously.
    """
    draw_bg.bg_y += bg_scroll_speed
    if draw_bg.bg_y >= background.get_height():
        draw_bg.bg_y = 0

    screen.blit(background, (0, draw_bg.bg_y))
    screen.blit(background, (0, draw_bg.bg_y - background.get_height()))
draw_bg.bg_y = 0


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def spawn_bullet(x, y, mode=1):
    for offset, m in bullet_mode_dict.get(mode, []):
        b = Bullet(x + offset, y, m)
        sprite_groups['bullet'].add(b)


def create_aliens_grid(row, col):
    interval = screen_width // (col + 1)
    for r in range(row):
        for c in range(col):
            alien = Alien(interval + c * interval, 100 + r * 70)
            sprite_groups['alien'].add(alien)


def spawn_aliens():
    spawn_aliens.countdown -= 1
    if spawn_aliens.countdown > 0:
        return
    spawn_aliens.countdown = spawn_aliens.cooldown
    alien = Alien(random.randint(50, screen_width - 50), random.randint(50, screen_height - 300))
    sprite_groups['alien'].add(alien)

    # decrease cooldown to increase difficulty over every 5 spawns
    spawn_aliens.repeat -= 1
    if spawn_aliens.repeat > 0:
        return
    spawn_aliens.repeat = spawn_alien_repeat
    spawn_aliens.cooldown = max(C.SPAWN_ALIEN_COOLDOWN_MIN, spawn_aliens.cooldown - C.SPAWN_ALIEN_COOLDOWN_DECREASE)
spawn_aliens.countdown = C.SPAWN_ALIEN_COOLDOWN
spawn_aliens.cooldown = C.SPAWN_ALIEN_COOLDOWN
spawn_aliens.repeat = spawn_alien_repeat


def spawn_aliens_teams(number, place=0):
    x, y, vx, vy, fig, is_flip = C.SPAWN_ALIENS_TEAMS_MAP[place]
    for i in range(number):
        sprite_groups['alien'].add(PassByAlien(x - vx * 15 * i, y - vy * 15 * i, vx, vy, fig, is_flip))


def spawn_alien_bullet(unbreakable=False):
    random_alien = random.choice(sprite_groups['alien'].sprites())
    if not unbreakable:
        sprite_groups['alien_bullet'].add(Alien_Bullet(random_alien.rect.centerx, random_alien.rect.bottom))
    else:
        sprite_groups['unbreakable_bullet'].add(Alien_Bullet(random_alien.rect.centerx, random_alien.rect.bottom, bu_type=1))


def spawn_powerups():
    spawn_powerups.countdown -= 1
    if spawn_powerups.countdown > 0:
        return
    spawn_powerups.countdown = random.randint(powerup_spawn_time, powerup_spawn_time + 200)
    powerup_type = random.choice([1, 2, 3, 4])
    powerup = Powerup(random.randint(50, screen_width - 50), -50, powerup_type)
    sprite_groups['powerup'].add(powerup)
spawn_powerups.countdown = powerup_spawn_time


def spawn_hong_bao():
    spawn_hong_bao.countdown -= 1
    if spawn_hong_bao.countdown > 0:
        return
    spawn_hong_bao.countdown = random.randint(60, hong_bao_spawn_time)
    spawn_hong_bao.countdown = max(60, spawn_hong_bao.countdown - hong_bao_collected)
    hong_bao = Hong_bao(random.randint(50, screen_width - 50), -50)
    sprite_groups['hong_bao'].add(hong_bao)
spawn_hong_bao.countdown = hong_bao_spawn_time


def spawn_boss(x, y, health, speed, fig, shot_cd, shot_cnt, shot_rest):
    boss = Boss(x, y, health, speed, fig, shot_cd, shot_cnt, shot_rest)
    sprite_groups['boss'].add(boss)


def spawn_boss_bullet():
    for bo in sprite_groups['boss'].sprites():
        time_now = pygame.time.get_ticks()
        if time_now - bo.last_shot > bo.shot_cd:
            if bo.shot_counter < bo.shot_cnt:
                bo.shot_counter += 1
                sprite_groups['unbreakable_bullet'].add(Alien_Bullet(bo.rect.centerx, bo.rect.bottom, bu_type=1))
                sprite_groups['alien_bullet'].add(Alien_Bullet(bo.rect.centerx - 20, bo.rect.bottom, mode=1))
                sprite_groups['alien_bullet'].add(Alien_Bullet(bo.rect.centerx + 20, bo.rect.bottom, mode=2))
                bo.last_shot = time_now
            else:
                bo.shot_counter = 0
                bo.last_shot = time_now + bo.shot_rest


def initialize_game():
    # create player spaceship
    spaceship = Spaceship(screen_width // 2, screen_height - 100, spaceship_health, spawn_bullet)
    sprite_groups['spaceship'].add(spaceship)


def load_phase(game_phase):
    with open(f"./phases/phase{game_phase}.json", 'r') as f:
        phase_data = json.load(f)
    
    return phase_data







# main game loop
initialize_game()
run = True
while run:
    
    clock.tick(fps)
    draw_bg()

    if countdown > 0:
        draw_text("GET READY!", font40, white, screen_width // 2 - 100, screen_height // 2 + 50)
        draw_text(str(countdown), font40, white, screen_width // 2 - 10, screen_height // 2 + 100)
        time_now = pygame.time.get_ticks()
        if time_now - last_countdown > 1000:
            countdown -= 1
            last_countdown = time_now


    if countdown == 0:

        # Check Game Over
        if len(sprite_groups['spaceship']) == 0:
            game_over = -1
        # if game_phase >= 5:
        #     C.SPAWN_ALIEN_COOLDOWN_MIN = 1
        if game_phase >= 5:
            game_over = 1

        # Start
        if game_over == 0:

            if state == 0:
                state += 1
                phase_data = load_phase(game_phase)
            if state == 1:
                state += 1
                if phase_data['data']['init'] == 1:
                    temp = phase_data['data']['init_data']['create_aliens_grid']
                    if len(temp) > 0:
                        create_aliens_grid(temp[0], temp[1])
                    for b in phase_data['data']['init_data']['spawn_boss']:
                        spawn_boss(screen_width // 2 + b['pos'][0], 
                                   b['pos'][1], 
                                   b['health'], 
                                   b['speed'], 
                                   b['fig'], 
                                   b['shot_cd'], 
                                   b['shot_cnt'], 
                                   b['shot_rest']
                        )
                        boss_wave_active = True
                        
            spawn_powerups()
            spawn_hong_bao()
            spawn_aliens()    
            if phase_data['data']['spawn_aliens_teams'] != -1:
                time_now = pygame.time.get_ticks()
                if time_now - last_alien_team > C.SPAWN_ALIENS_TEAMS_COOLDOWN:
                    spawn_aliens_teams(5, random.randint(0, len(C.SPAWN_ALIENS_TEAMS_MAP) - 1))
                    last_alien_team = time_now
            spawn_boss_bullet()


            # create random alien bullets
            time_now = pygame.time.get_ticks()
            if time_now - last_alien_shot > C.ALIEN_SHOT_COOLDOWN:
                for _ in range(len(sprite_groups['alien']) // C.ALIEN_SHOT_RATIO):
                    spawn_alien_bullet()
                for _ in range(len(sprite_groups['alien']) // C.ALIEN_UNBREAKABLE_SHOT_RATIO):
                    spawn_alien_bullet(unbreakable=True)
                last_alien_shot = time_now

            # update sprite group
            for k in sprite_groups:
                if k != 'explosion':
                    sprite_groups[k].update()

            # check for collisions
            collision_results = resolve_all(
                sprite_groups,
                sound_manager,
            )
            killed_aliens += collision_results['killed_aliens']
            hong_bao_collected += collision_results['hong_bao_collected']
            # PowerUP Effect Resolver
            for ship, pu_type in collision_results['applied_powerups']:
                if pu_type == 1:
                    ship.health_start += C.POWERUP_RECOVER_HEALTH
                    ship.health_remaining += C.POWERUP_RECOVER_HEALTH
                elif pu_type == 2:
                    # ship.bullet_cooldown = max(C.POWERUP_COOLDOWN_MIN, ship.bullet_cooldown - C.POWERUP_DECREASE_COOLDOWN)
                    ship.bullet_cd_state += 1
                elif pu_type == 3:
                    if ship.mode < len(bullet_mode_dict):
                        ship.mode += 1
                        ship.bullet_cd_state -= 1 # mode increase too unbalanced so make culldown longer
                    else:
                        # ship.bullet_cooldown = max(C.POWERUP_COOLDOWN_MIN, ship.bullet_cooldown - C.POWERUP_DECREASE_COOLDOWN)
                        ship.bullet_cd_state += 1
                elif pu_type == 4:
                    sprite_groups['sword'].add(Sword(sprite_groups['spaceship'].sprites()[0], angle=math.pi * 1.5))
                    sprite_groups['sword'].add(Sword(sprite_groups['spaceship'].sprites()[0], angle=math.pi * 0.5))


            # Check Phase Transition
            if boss_wave_active and len(sprite_groups['boss']) == 0:
                boss_wave_active = False
                game_phase += 1
                state = 0
            temp = phase_data['data']['end']['killed_aliens']
            if temp != -1 and killed_aliens >= temp:
                game_phase += 1
                state = 0
            


        # update explosion group (do this regardless of game over so explosions can finish)
        sprite_groups['explosion'].update()

    # draw sprite groups
    for k in sprite_groups:
        if k != 'spaceship' and k != 'boss':
            sprite_groups[k].draw(screen)
        else:
            sprite_groups[k].draw(screen)
            for obj in sprite_groups[k].sprites():
                obj.draw_healthbar(screen)

    draw_text("aliens killed: {0}".format(killed_aliens), font20, white, screen_width // 2 + 100, 20)
    draw_text("hong bao collected: {0}".format(hong_bao_collected), font20, white, screen_width // 2 + 100, 50)
    if len(sprite_groups['spaceship']) > 0:
        s = sprite_groups['spaceship'].sprites()[0]
        draw_text("heath: {0} / {1}".format(s.health_remaining, s.health_start), font20, white, screen_width // 2 + 100, 80)
    if game_over == -1:
        draw_text("GAME OVER!", font40, white, screen_width // 2 - 120, screen_height // 2 + 50)
    if game_over == 1:
        draw_text("YOU WIN!", font40, white, screen_width // 2 - 100, screen_height // 2 + 50)
        draw_text("hong bao collected: {0}".format(hong_bao_collected), font30, white, screen_width // 2 - 100, screen_height // 2 + 100)

    # create event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()