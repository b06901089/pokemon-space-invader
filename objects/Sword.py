import pygame
import math
import config.constant as C

class Sword(pygame.sprite.Sprite):
    def __init__(self, target, angle=0.0, damage_cooldown=30):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        img = pygame.image.load(C.SWORD_PATH)
        img = pygame.transform.scale(img, (32, 32))
        self.image = pygame.transform.rotate(img, 45)
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.centerx = self.target.rect.centerx + C.SWORD_RANGE * math.cos(self.angle)
        self.rect.centery = self.target.rect.centery + C.SWORD_RANGE * math.sin(self.angle)
        self.power = 1
        
        # Damage cooldown tracking: {enemy_id: frame_count}
        # This prevents the same enemy from taking damage every frame
        self.last_hit_frame = {}  # Maps id(enemy) to the frame when it was last hit
        self.damage_cooldown = damage_cooldown  # Frames between damage to same enemy
    
    def update(self):
        self.angle += math.pi / 240.0
        self.rect.centerx = self.target.rect.centerx + C.SWORD_RANGE * math.cos(self.angle)
        self.rect.centery = self.target.rect.centery + C.SWORD_RANGE * math.sin(self.angle)
    
    def can_damage(self, enemy, current_frame):
        """Check if this enemy can be damaged by the sword now.
        
        Args:
            enemy: The enemy sprite to check
            current_frame: The current game frame number
            
        Returns:
            True if the enemy can be damaged, False if still in cooldown
        """
        enemy_id = id(enemy)
        
        # If enemy was never hit, allow damage
        if enemy_id not in self.last_hit_frame:
            self.last_hit_frame[enemy_id] = current_frame
            return True
        
        # Check if cooldown period has passed
        frames_since_hit = current_frame - self.last_hit_frame[enemy_id]
        if frames_since_hit >= self.damage_cooldown:
            self.last_hit_frame[enemy_id] = current_frame
            return True
        
        return False
