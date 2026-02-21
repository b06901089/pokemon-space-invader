import pygame
import random
import math
import config.constant as C

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_tpye=-1, speed_dir=(-1, -1, -1), alien_figure=None):
        pygame.sprite.Sprite.__init__(self)
        if not alien_figure:
            self.image = pygame.image.load(C.ORG_ALIEN_PATH[random.randint(0, 4)])
        else:
            self.image = pygame.image.load(C.POKEMON_PATH[alien_figure])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = [float(self.rect.x), float(self.rect.y)]

        if alien_tpye == -1:
            self.speed = random.uniform(0.8, 2.0)
            self.vx = 0.0
            self.vy = 2.0
            self.pick_new_direction()
        else:
            self.speed = speed_dir[0]
            self.vx = speed_dir[1]
            self.vy = speed_dir[2]


    def pick_new_direction(self, hit_left=False, hit_right=False, hit_top=False, hit_bottom=False):
        """Choose a new random direction that points away from the wall hit.

        Assumes at most one side is hit (common in practice). For each side we
        pick an angle range that guarantees the resulting velocity points away
        from that side. If multiple sides are reported, fall back to an
        unconstrained random direction.
        """
        # Count how many sides were hit; if multiple, use unconstrained angle
        hits = sum(bool(f) for f in (hit_left, hit_right, hit_top, hit_bottom))

        if hits == 1:
            if hit_top:
                # want vy > 0 (move downward): angles in (0, pi)
                angle = random.uniform(0, math.pi)
            elif hit_bottom:
                # want vy < 0 (move upward): angles in (pi, 2*pi)
                angle = random.uniform(math.pi, 2 * math.pi)
            elif hit_left:
                # want vx > 0 (move right): angles in (-pi/2, pi/2)
                # represent as two ranges [0, pi/2) U (3pi/2, 2pi)
                if random.random() < 0.5:
                    angle = random.uniform(0, math.pi / 2)
                else:
                    angle = random.uniform(3 * math.pi / 2, 2 * math.pi)
            else:  # hit_right
                # want vx < 0 (move left): angles in (pi/2, 3pi/2)
                angle = random.uniform(math.pi / 2, 3 * math.pi / 2)
        else:
            # fallback: unconstrained direction
            angle = random.uniform(0, 2 * math.pi)

        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

    def update(self):
        # move using float position then update rect
        self.pos[0] += self.vx
        self.pos[1] += self.vy

        # write back to rect
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])

        # if we hit a screen boundary, snap back inside and pick a new direction
        hit_left = False
        hit_right = False
        hit_top = False
        hit_bottom = False

        if self.rect.left <= 0:
            self.pos[0] = 0
            hit_left = True
        if self.rect.right >= C.SCREEN_WIDTH:
            self.pos[0] = C.SCREEN_WIDTH - self.rect.width
            hit_right = True
        if self.rect.top <= 0:
            self.pos[1] = 0
            hit_top = True
        if self.rect.bottom >= C.SCREEN_HEIGHT:
            self.pos[1] = C.SCREEN_HEIGHT - self.rect.height
            hit_bottom = True

        if hit_left or hit_right or hit_top or hit_bottom:
            self.pick_new_direction(hit_left=hit_left, hit_right=hit_right,
                                     hit_top=hit_top, hit_bottom=hit_bottom)
            
    
class PassByAlien(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, alien_figure=None, is_flip=False):
        pygame.sprite.Sprite.__init__(self)
        if not alien_figure:
            self.image = pygame.image.load(C.ORG_ALIEN_PATH[random.randint(0, 4)])
        else:
            self.image = pygame.image.load(C.POKEMON_PATH[alien_figure])
        if is_flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # self.pos = [float(self.rect.x), float(self.rect.y)]

        self.vx = vx
        self.vy = vy

        self.active = False

    def update(self):
        # self.pos[0] += self.vx
        # self.pos[1] += self.vy
        # self.rect.x = int(self.pos[0])
        # self.rect.y = int(self.pos[1])
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.top > C.SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > C.SCREEN_WIDTH:
            if self.active:
                self.kill()
        else:
            self.active = True