import random
import config.constant as C

def get_random_x():
    return random.randint(0, C.SCREEN_WIDTH)

def get_random_coord_infront_of_sprite(sprite, distance, box_width, box_height):
    x = sprite.rect.centerx
    y = sprite.rect.centery

    half_width = box_width // 2
    half_height = box_height // 2
    offset_x = random.randint(-half_width, half_width)
    offset_y = random.randint(-half_height, half_height)
    
    x = x + offset_x
    y = y + offset_y + distance
    
    return x, y

def is_too_close_to_mypoke(mypoke, x, y, exclusion_radius_2=14400):
    dx = x - mypoke.rect.centerx
    dy = y - mypoke.rect.centery
    distance = (dx ** 2 + dy ** 2)
    
    return distance < exclusion_radius_2

def get_animation_spawn_location(sprite_groups, sprite, spawn_dir, spawn_ops):
    if spawn_ops:
        if spawn_dir == "self":
            x = sprite.rect.centerx
            y = sprite.rect.top
        elif spawn_dir == "rdm_top":
            x = get_random_x()
            y = C.SCREEN_HEIGHT + 50
        elif spawn_dir == "full_rdm":
            raise ValueError("Current spawn_dir is Not Supported!")
        elif spawn_dir == "infront_rdm_mid":
            x, y = get_random_coord_infront_of_sprite(sprite, -350, 200, 250)
        else:
            raise ValueError("Current spawn_dir is Not Supported!")
    else:
        if spawn_dir == "self":
            x = sprite.rect.centerx
            y = sprite.rect.bottom
        elif spawn_dir == "rdm_top":
            x = get_random_x()
            y = -50
        elif spawn_dir == "full_rdm":
            max_attempts = 20
            attempts = 0
            while attempts < max_attempts:
                x = random.randint(32, C.SCREEN_WIDTH - 32)
                y = random.randint(32, C.SCREEN_HEIGHT + 32)
                if sprite_groups['mypoke'] and not is_too_close_to_mypoke(sprite_groups['mypoke'].sprites()[0], x, y, exclusion_radius_2=14400):
                    break
                attempts += 1
        elif spawn_dir == "infront_rdm_mid":
            x, y = get_random_coord_infront_of_sprite(sprite, 350, 200, 250)
        else:
            raise ValueError("Current spawn_dir is Not Supported!")

    return x, y