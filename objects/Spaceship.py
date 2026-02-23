### Deprecated

# import pygame
# import config.constant as C

# from config import sound_manager

# class Spaceship(pygame.sprite.Sprite):
#     def __init__(self, x, y, health, spawn_bullet):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load(C.SPACESHIP_PATH)
#         self.mask = pygame.mask.from_surface(self.image)
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)
#         self.health_start = health
#         self.health_remaining = health
#         self.spaceship_speed = C.SPACESHIP_SPEED
#         self.last_shot = pygame.time.get_ticks()
#         self.bullet_cooldown = C.BULLET_COOLDOWN
#         self.bullet_cd_state = 0
#         self.spawn_bullet = spawn_bullet
#         self.mode = 1

#     def draw_healthbar(self, surface):
#         pygame.draw.rect(surface, C.RED, (self.rect.x, self.rect.bottom + 5, self.rect.width, 5))
#         if self.health_remaining > 0:
#             pygame.draw.rect(surface, C.GREEN, (self.rect.x, self.rect.bottom + 5, int(self.rect.width * (self.health_remaining / self.health_start)), 5))

#     def update(self):        
#         key = pygame.key.get_pressed()
#         if key[pygame.K_LEFT] and self.rect.left > 0:
#             self.rect.x -= self.spaceship_speed
#         if key[pygame.K_RIGHT] and self.rect.right < C.SCREEN_WIDTH:
#             self.rect.x += self.spaceship_speed
#         if key[pygame.K_UP] and self.rect.top > 0:
#             self.rect.y -= self.spaceship_speed
#         if key[pygame.K_DOWN] and self.rect.bottom < C.SCREEN_HEIGHT:
#             self.rect.y += self.spaceship_speed
            
#         # shoot bullet
#         time_now = pygame.time.get_ticks()
#         if key[pygame.K_SPACE] and time_now - self.last_shot > self.bullet_cooldown - C.POWERUP_BULLET_CD[max(min(len(C.POWERUP_BULLET_CD) - 1, self.bullet_cd_state), 0)]:
#             sound_manager.play("laser")
#             self.spawn_bullet(self.rect.centerx, self.rect.top, self.mode)
#             self.last_shot = time_now

#         if self.health_remaining <= 0:
#             self.kill()
#             sound_manager.play("explosion2")