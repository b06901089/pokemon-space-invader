import pygame
import config.constant as C

from objects import *

def spawn_boss(sprite_groups, x, y, health, speed, fig, shot_cd, shot_cnt, shot_rest):
    boss = Boss(x, y, health, speed, fig, shot_cd, shot_cnt, shot_rest)
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

def spawn_aliens_teams(sprite_groups, last_alien_team, number, which_team):
    time_now = pygame.time.get_ticks()
    if time_now - last_alien_team > C.SPAWN_ALIENS_TEAMS_COOLDOWN:
        x, y, vx, vy, fig, is_flip = C.SPAWN_ALIENS_TEAMS_MAP[which_team]
        for i in range(number):
            sprite_groups['alien'].add(PassByAlien(x - vx * 15 * i, y - vy * 15 * i, vx, vy, fig, is_flip))
        return time_now
    return last_alien_team