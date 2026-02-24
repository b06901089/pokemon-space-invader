import pygame
import random
import math
import config.constant as C


from objects import *
from config import sound_manager
from collisions import resolve_all
from scripts.utils import *
from items_menu import show_items_menu


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)


sound_manager.load("explosion", "img/org_space_invader/explosion.wav")
sound_manager.load("explosion2", "img/org_space_invader/explosion2.wav")
sound_manager.load("laser", "img/org_space_invader/laser.wav")


# define constants
powerup_spawn_time = C.POWERUP_SPAWN_TIME
screen_width = C.SCREEN_WIDTH
screen_height = C.SCREEN_HEIGHT
game_title = C.GAME_TITLE
red = C.RED
green = C.GREEN
blue = C.BLUE
white = C.WHITE
spawn_alien_repeat = C.SPAWN_ALIEN_REPEAT
hong_bao_spawn_time = C.HONG_BAO_SPAWN_TIME
bg_scroll_speed = 1  # pixels per frame;
spaceship_fire_modes = 2 # temp


# define other game variables
last_alien_shot = pygame.time.get_ticks()
last_boss_shot = pygame.time.get_ticks()
last_countdown = pygame.time.get_ticks()
last_alien_team = pygame.time.get_ticks()
countdown = 3
game_phase = 2 # modify this to test different phases directly
state = 0
killed_aliens = 0
game_over = 0 # 0 is game not over, 1 is player has won, -1 is player has lost
hong_bao_collected = 0
powerup_collected = 0
boss_wave_active = False
schedulers_list = []

# simple UI: panel for 3-item choice and panel for inventory
phase_choice_visible = False


# define FPS
clock = pygame.time.Clock()
fps = 60


# create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(game_title)


# loading background image
background = pygame.image.load("img/org_space_invader/bg.png")


# define font
font10 = pygame.font.SysFont("Constantia", 10)
font20 = pygame.font.SysFont("Constantia", 20)
font30 = pygame.font.SysFont("Constantia", 30)
font40 = pygame.font.SysFont("Constantia", 40)


# create sprites groups
sprite_groups = {
    'mypoke': pygame.sprite.Group(),
    'my_ani': pygame.sprite.Group(),
    'alien': pygame.sprite.Group(),
    # 'alien_bullet': pygame.sprite.Group(),
    # 'unbreakable_bullet': pygame.sprite.Group(),
    'explosion': pygame.sprite.Group(),
    'powerup': pygame.sprite.Group(),
    'boss': pygame.sprite.Group(),
    'hong_bao': pygame.sprite.Group(),
    'sword': pygame.sprite.Group(),
    'animation': pygame.sprite.Group(),
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


def initialize_game():
    starting_poke = MyPokemon(
        screen_width // 2, 
        screen_height - 100, 
        'spaceship', 
        'shoot_type_1_mode_1',
        sprite_groups,
        spawn_animation_for_sprite,
        schedulers_list
    )
    sprite_groups['mypoke'].add(starting_poke)


# show items/powerups UI before starting the game
show_items_menu(screen)

# main game loop
initialize_game()
phase_choice_panel, phase_choice_rects = render_item_choice_panel()
inventory_panel, inventory_rects = render_inventory_panel()
my_inventory = Inventory()
run = True
while run:
    
    clock.tick(fps)
    draw_bg()

    if countdown > 0:
        draw_text(screen, "GET READY!", font40, white, screen_width // 2 - 100, screen_height // 2 + 50)
        draw_text(screen, str(countdown), font40, white, screen_width // 2 - 10, screen_height // 2 + 100)
        time_now = pygame.time.get_ticks()
        if time_now - last_countdown > 1000:
            countdown -= 1
            last_countdown = time_now

    if countdown == 0 and not phase_choice_visible:

        # Check Game Over
        if len(sprite_groups['mypoke']) == 0:
            game_over = -1
        if game_phase >= 5:
            game_over = 1

        # Start
        if game_over == 0:

            if state == 0:
                phase_data = load_phase(game_phase)
                phase_choice_visible = True
                item_rewards = get_random_three_items()
            if state == 1:
                state += 1
                if phase_data['data']['init'] == 1:
                    temp = phase_data['data']['init_data']['create_aliens_grid']
                    if len(temp) > 0:
                        create_aliens_grid(sprite_groups, temp[0], temp[1])
                    for b in phase_data['data']['init_data']['spawn_boss']:
                        spawn_boss(sprite_groups,
                                   screen_width // 2 + b['pos'][0], 
                                   b['pos'][1], 
                                   b['health'], 
                                   b['speed'], 
                                   b['fig'],
                                   b['moves']
                        )
                        boss_wave_active = True

            schedulers_list = [s for s in schedulers_list if s.update()]

            # Execute moves for all sprites with moves
            execute_sprite_moves(sprite_groups['boss'], sprite_groups, schedulers_list)
            execute_sprite_moves(sprite_groups['alien'], sprite_groups, schedulers_list)

            spawn_hong_bao()
            spawn_aliens()  
            if powerup_collected < phase_data['data']['powerup_cnt_limit']:
                spawn_powerups()  

            # update sprite group
            for k in sprite_groups:
                if k != 'explosion' and k != 'animation':
                    sprite_groups[k].update()

            # check for collisions
            collision_results = resolve_all(
                sprite_groups,
                sound_manager,
            )
            killed_aliens += collision_results['killed_aliens']
            hong_bao_collected += collision_results['hong_bao_collected']
            # PowerUP Effect Resolver
            powerup_collected += len(collision_results['applied_powerups'])
            for ship, pu_type in collision_results['applied_powerups']:
                if pu_type == 1:
                    ship.health_start += C.POWERUP_RECOVER_HEALTH
                    ship.health_remaining += C.POWERUP_RECOVER_HEALTH
                elif pu_type == 2:
                    ship.move_cd_state += 1
                elif pu_type == 3:
                    ship.move_cd_state += 1
                    # if ship.mode < spaceship_fire_modes:
                    #     ship.mode += 1
                    # else:
                    #     ship.move_cd_state += 1
                elif pu_type == 4:
                    sprite_groups['sword'].add(Sword(sprite_groups['mypoke'].sprites()[0], angle=math.pi * 1.5))
                    sprite_groups['sword'].add(Sword(sprite_groups['mypoke'].sprites()[0], angle=math.pi * 0.5))


            # Check Phase Transition
            if boss_wave_active and len(sprite_groups['boss']) == 0:
                boss_wave_active = False
                game_phase += 1
                state = 0
            temp = phase_data['data']['end']['killed_aliens']
            if temp != -1 and killed_aliens >= temp:
                game_phase += 1
                state = 0
            

        # update explosion and animation group (do this regardless of game over so explosions can finish)
        sprite_groups['explosion'].update()
        sprite_groups['animation'].update()

    # draw sprite groups
    for k in sprite_groups:
        sprite_groups[k].draw(screen)
        if k == 'mypoke' or k == 'boss':
            for obj in sprite_groups[k].sprites():
                obj.draw_healthbar(screen)

    draw_text(screen, "aliens killed: {0}".format(killed_aliens), font20, white, screen_width // 2 + 100, 20)
    draw_text(screen, "hong bao collected: {0}".format(hong_bao_collected), font20, white, screen_width // 2 + 100, 50)
    if len(sprite_groups['mypoke']) > 0:
        s = sprite_groups['mypoke'].sprites()[0]
        draw_text(screen, "heath: {0} / {1}".format(s.health_remaining, s.health_start), font20, white, screen_width // 2 + 100, 80)
    if game_over == -1:
        draw_text(screen, "GAME OVER!", font40, white, screen_width // 2 - 120, screen_height // 2 + 50)
    if game_over == 1:
        draw_text(screen, "YOU WIN!", font40, white, screen_width // 2 - 100, screen_height // 2 + 50)
        draw_text(screen, "hong bao collected: {0}".format(hong_bao_collected), font30, white, screen_width // 2 - 100, screen_height // 2 + 100)

    if phase_choice_visible:
        # panel background
        pygame.draw.rect(screen, (30, 30, 30), phase_choice_panel)
        pygame.draw.rect(screen, (200, 200, 200), phase_choice_panel, 4)
        # inner boxes
        for idx, r in enumerate(phase_choice_rects):
            pygame.draw.rect(screen, (60, 60, 60), r)
            pygame.draw.rect(screen, (220, 220, 220), r, 3)
            draw_text(screen, item_rewards[idx], font20, white, r.x + 10, r.y + r.height - 30)
            image_surface = pygame.image.load(C.ITEM_JSON[item_rewards[idx]]['url']).convert_alpha() 
            image_rect = image_surface.get_rect()
            image_rect.center = r.center
            screen.blit(image_surface, image_rect)

    # inventory panel (render-only)
    pygame.draw.rect(screen, (24, 24, 24), inventory_panel)
    pygame.draw.rect(screen, (180, 180, 180), inventory_panel, 1)
    items = my_inventory.get_inventory()
    for i in range(6):
        pygame.draw.rect(screen, (48, 48, 48), inventory_rects[i])
        pygame.draw.rect(screen, (200, 200, 200), inventory_rects[i], 1)
        draw_text(screen, C.INVENTORY_SHOW_KEY[i], font10, white, inventory_rects[i].x + 24, inventory_rects[i].y + 20)
        if items[i][0] is not None:
            image_surface = pygame.image.load(C.ITEM_JSON[items[i][0]]['url']).convert_alpha() 
            image_rect = image_surface.get_rect()
            image_rect.center = inventory_rects[i].center
            screen.blit(image_surface, image_rect)
            draw_text(screen, "x{0}".format(items[i][1]), font10, white, inventory_rects[i].x + 4, inventory_rects[i].y + 20)

    # create event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONUP and phase_choice_visible:
            pos = pygame.mouse.get_pos()
            clicked_idx = None
            for i, r in enumerate(phase_choice_rects):
                if r.collidepoint(pos):
                    clicked_idx = i
                    my_inventory.add_item(item_rewards[i])
                    break
            if clicked_idx is not None:
                phase_choice_visible = False
                state += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                my_inventory.use_item(0, sprite_groups['mypoke'].sprites()[0])
            elif event.key == pygame.K_w:
                my_inventory.use_item(1, sprite_groups['mypoke'].sprites()[0])
            elif event.key == pygame.K_e:
                my_inventory.use_item(2, sprite_groups['mypoke'].sprites()[0])
            elif event.key == pygame.K_a:
                my_inventory.use_item(3, sprite_groups['mypoke'].sprites()[0])
            elif event.key == pygame.K_s:
                my_inventory.use_item(4, sprite_groups['mypoke'].sprites()[0])
            elif event.key == pygame.K_d:
                my_inventory.use_item(5, sprite_groups['mypoke'].sprites()[0])

    pygame.display.update()

pygame.quit()