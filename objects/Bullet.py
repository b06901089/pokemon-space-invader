import pygame
import config.constant as C

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mode=0):
        pygame.sprite.Sprite.__init__(self)
        # load with per-pixel alpha and tweak visuals to be less distracting
        image = pygame.image.load("img/bullet.png").convert_alpha()

        # # Optional: scale down slightly to be less visually dominant
        # orig_w, orig_h = image.get_size()
        # scale_factor = 0.9  # tweak to make bullets smaller or larger
        # if scale_factor != 1.0:
        #     image = pygame.transform.smoothscale(image, (int(orig_w * scale_factor), int(orig_h * scale_factor)))

        # Apply a soft tint (multiply) and make semi-transparent
        tint_color = (150, 200, 255)  # light bluish tint; tweak as desired
        tint_surf = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        tint_surf.fill((*tint_color, 255))
        image.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Overall transparency: 0 (invisible) .. 255 (opaque)
        image.set_alpha(180)  # lower makes it more transparent

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.bullet_dir = C.BULLET_DIR[mode]

    def update(self):
        self.rect.x -= self.bullet_dir
        self.rect.y -= 7

        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > C.SCREEN_WIDTH:
            self.kill()