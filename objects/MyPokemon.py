import pygame
import config.constant as C
import re

from config import sound_manager

class MyPokemon(pygame.sprite.Sprite):
    def __init__(self, x, y, name, move, sprite_groups, spawn_animation_for_sprite, schedulers_list):
        pygame.sprite.Sprite.__init__(self)
        data = C.POKE_JSON[name]
        self.name = name
        self.image = pygame.image.load(data['url'])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health_start = data['health']
        self.health_remaining = data['health']
        self.velocity = data['velocity']
        self.last_move_time = pygame.time.get_ticks()
        self.move = move
        self.move_cd = data['move_cd']
        self.move_cd_state = 0
        self.sprite_groups = sprite_groups
        self.spawn_animation_for_sprite = spawn_animation_for_sprite
        self.schedulers_list = schedulers_list

    def draw_healthbar(self, surface):
        pygame.draw.rect(surface, C.RED, (self.rect.x, self.rect.bottom + 5, self.rect.width, 5))
        if self.health_remaining > 0:
            pygame.draw.rect(surface, C.GREEN, (self.rect.x, self.rect.bottom + 5, int(self.rect.width * (self.health_remaining / self.health_start)), 5))

    def update_move(self):
        m = re.search(r"(.*_mode_)(\d+)$", self.move)
        if m:
            prefix, num = m.groups()
            new_move = f"{prefix}{int(num) + 1}"
            if new_move in C.MOVE_JSON['moves'].keys():
                self.move = new_move
                print(new_move)
                return True
        return False 

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if key[pygame.K_RIGHT] and self.rect.right < C.SCREEN_WIDTH:
            self.rect.x += self.velocity
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocity
        if key[pygame.K_DOWN] and self.rect.bottom < C.SCREEN_HEIGHT:
            self.rect.y += self.velocity

        # move
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_move_time > self.move_cd[max(min(self.move_cd_state, len(self.move_cd) - 1), 0)]:
            sound_manager.play("laser")
            self.spawn_animation_for_sprite(
                self.sprite_groups,
                self,
                self.move,
                "self",
                True,
                self.schedulers_list
            )
            self.last_move_time = time_now
    
        if self.health_remaining <= 0:
            self.kill()
            sound_manager.play("explosion2")