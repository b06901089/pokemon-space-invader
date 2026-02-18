import pygame
import json
import random
import config.constant as C

from objects import *

def get_random_x():
    return random.randint(0, C.SCREEN_WIDTH)

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def spawn_boss(sprite_groups, x, y, health, speed, fig, shot_cd, shot_cnt, shot_rest, moves):
    boss = Boss(x, y, health, speed, fig, shot_cd, shot_cnt, shot_rest, moves)
    sprite_groups['boss'].add(boss)

def spawn_boss_bullet(sprite_groups):
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

def spawn_animation_for_sprite(sprite_groups, sprite, ani, spawn_dir, ani_part, replicas_list):
    if spawn_dir == "rdm_top":
        x = get_random_x()
        y = -50
    elif spawn_dir == "self":
        x = sprite.rect.centerx
        y = sprite.rect.centery
        
    for idx in range(ani_part):
        sprite_groups['animation'].add(Animation(x, y, ani, idx))
        rep = C.MOVE_JSON['moves'][ani][idx]['replicas']
        rep_delay = C.MOVE_JSON['moves'][ani][idx]['replica_delay']
        if rep > 0:
            replicas_list.append([0, rep, rep_delay, (x, y, ani, idx)])

def spawn_aliens_teams(sprite_groups, last_alien_team, number, which_team):
    time_now = pygame.time.get_ticks()
    if time_now - last_alien_team > C.SPAWN_ALIENS_TEAMS_COOLDOWN:
        x, y, vx, vy, fig, is_flip = C.SPAWN_ALIENS_TEAMS_MAP[which_team]
        for i in range(number):
            sprite_groups['alien'].add(PassByAlien(x - vx * 15 * i, y - vy * 15 * i, vx, vy, fig, is_flip))
        return time_now
    return last_alien_team

def spawn_alien_bullet(sprite_groups, unbreakable=False):
    random_alien = random.choice(sprite_groups['alien'].sprites())
    if not unbreakable:
        sprite_groups['alien_bullet'].add(Alien_Bullet(random_alien.rect.centerx, random_alien.rect.bottom))
    else:
        sprite_groups['unbreakable_bullet'].add(Alien_Bullet(random_alien.rect.centerx, random_alien.rect.bottom, bu_type=1))

def create_aliens_grid(sprite_groups, row, col):
    interval = C.SCREEN_WIDTH // (col + 1)
    for r in range(row):
        for c in range(col):
            sprite_groups['alien'].add(Alien(interval + c * interval, 100 + r * 70))

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def load_phase(game_phase):
    with open(f"./phases/phase{game_phase}.json", 'r') as f:
        return json.load(f)
    
def render_item_choice_panel():
    # prepare a centered panel and three inner boxes to render choices
    panel_w = 3 * 180 + 4 * 15
    panel_h = 200
    panel_x = (C.SCREEN_WIDTH - panel_w) // 2
    panel_y = (C.SCREEN_HEIGHT - panel_h) // 2
    phase_choice_panel = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
   
    # inner boxes
    phase_choice_rects = []
    for i in range(3):
        bx = panel_x + i * (180 + 15) + 15
        by = panel_y + 20
        phase_choice_rects.append(pygame.Rect(bx, by, 180, 160))
    
    return phase_choice_panel, phase_choice_rects
