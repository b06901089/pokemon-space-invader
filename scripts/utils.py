import pygame
import json
import random
import config.constant as C

from objects import *

def get_random_x():
    return random.randint(0, C.SCREEN_WIDTH)

def is_too_close_to_spaceship(spaceship, x, y, exclusion_radius_2=14400):
    dx = x - spaceship.rect.centerx
    dy = y - spaceship.rect.centery
    distance = (dx ** 2 + dy ** 2)
    
    return distance < exclusion_radius_2

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def spawn_boss(sprite_groups, x, y, health, speed, fig, moves):
    boss = Boss(x, y, health, speed, fig, moves)
    sprite_groups['boss'].add(boss)

def spawn_animation_for_sprite(sprite_groups, sprite, ani, spawn_dir, spawn_ops, ani_part, schedulers_list):
    if spawn_dir == "rdm_top":
        x = get_random_x()
        y = -50
    elif spawn_dir == "self":
        x = sprite.rect.centerx
        if spawn_ops:
            y = sprite.rect.top
        else:
            y = sprite.rect.bottom
    elif spawn_dir == "full_rdm":
        max_attempts = 20
        attempts = 0
        while attempts < max_attempts:
            x = random.randint(32, C.SCREEN_WIDTH - 32)
            y = random.randint(32, C.SCREEN_HEIGHT + 32)
            if sprite_groups['spaceship'] and not is_too_close_to_spaceship(sprite_groups['spaceship'].sprites()[0], x, y, exclusion_radius_2=14400):
                break
            attempts += 1
    
    for idx in range(ani_part):   
        if spawn_ops:     
            sprite_groups['bullet'].add(Animation(x, y, ani, idx, spawn_ops))
        else:
            sprite_groups['animation'].add(Animation(x, y, ani, idx, spawn_ops))
        
        rep = C.MOVE_JSON['moves'][ani][idx]['replicas']
        rep_delay = C.MOVE_JSON['moves'][ani][idx]['replica_delay']
        if rep > 0:
            scheduler = ReplicaScheduler(sprite_groups, sprite, x, y, ani, idx, rep, rep_delay, spawn_dir, spawn_ops)
            schedulers_list.append(scheduler)

def execute_sprite_moves(sprite_group, sprite_groups, schedulers_list):
    time_now = pygame.time.get_ticks()
    for sprite in sprite_group.sprites():
        for move in sprite.moves:
            if time_now - move['last_move_time'] > move['freq']:
                move['last_move_time'] = time_now
                spawn_animation_for_sprite(
                    sprite_groups,
                    sprite,
                    move['name'],
                    move['spawn_dir'],
                    False,
                    len(C.MOVE_JSON['moves'][move['name']]),
                    schedulers_list
                )

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

def render_inventory_panel():
    # prepare a bottom-left panel and six inner boxes to render inventory
    box_w = 32
    box_h = 32
    cols = 3
    rows = 2
    padding = 2
    panel_w = box_w * cols + padding * (cols + 1)
    panel_h = box_h * rows + padding * (rows + 1)
    panel_x = 0
    panel_y = C.SCREEN_HEIGHT - panel_h
    inventory_panel = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
    
    # inner boxes
    inventory_rects = []
    for i in range(6):
        col = i % cols
        row = i // cols
        bx = panel_x + padding + col * (box_w + padding)
        by = panel_y + padding + row * (box_h + padding)
        inventory_rects.append(pygame.Rect(bx, by, box_w, box_h))
    
    return inventory_panel, inventory_rects

def get_random_three_items():

    keys = list(C.ITEM_JSON.keys())
    weights = C.ITEM_WEIGHTS

    scored = [
        (random.random() ** (1 / w), k)
        for k, w in zip(keys, weights)
    ]

    return [k for _, k in sorted(scored, reverse=True)[:3]]
    # return random.choices(list(C.ITEM_JSON.keys()), weights=C.ITEM_WEIGHTS, k=3) # this is with replacement, which means you can get duplicates.
    # return random.sample(list(C.ITEM_JSON.keys()), 3) # this doesn't consider weights.