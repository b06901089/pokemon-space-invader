import pygame
import random
import config.constant as C

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, health, speed, fig, moves):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(C.BOSS_PATH[fig][0])
        self.image = pygame.transform.scale(img, C.BOSS_PATH[fig][1])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health_start = health
        self.health_remaining = health
        self.move_speed = speed
        self.y_limit = C.SCREEN_HEIGHT // 2 - random.randint(0, 200)
        self.moves = moves
        self.movement = None
        self.movement_state = 0
        self.movement_state_id = 0

    def draw_healthbar(self, surface):
        pygame.draw.rect(surface, C.RED, (self.rect.x, self.rect.bottom + 5, self.rect.width, 5))
        if self.health_remaining > 0:
            pygame.draw.rect(surface, C.GREEN, (self.rect.x, self.rect.bottom + 5, int(self.rect.width * (self.health_remaining / self.health_start)), 5))

    def register_movement(self, move):
        if self.movement is None:
            self.movement, _ = self.parse_pre_move(C.PRE_MOVE_JSON[move])

    def parse_pre_move(self, lst):
        if len(lst) % 3 != 0:
            raise ValueError("List length must be a multiple of 3")
        rows = [lst[i:i+3] for i in range(0, len(lst), 3)]
        last_sum = sum(row[-1] for row in rows)

        return rows, last_sum

    def update(self):
        if self.movement is not None:
            state = self.movement[self.movement_state]
            self.rect.x += state[0]
            self.rect.y += state[1]
            self.movement_state_id += 1
            if self.movement_state_id >= state[2]:
                self.movement_state_id = 0
                self.movement_state += 1
                if self.movement_state >= len(self.movement):
                    self.movement_state = 0
                    self.movement = None
            return

        if self.rect.bottom <= self.y_limit:
            self.rect.y += self.move_speed
        else:
            if self.rect.left < 0:
                self.rect.left = 0
                self.move_speed *= -1
            elif self.rect.right > C.SCREEN_WIDTH:
                self.rect.right = C.SCREEN_WIDTH
                self.move_speed *= -1
            self.rect.x += self.move_speed