import pygame
from objects import Animation

class ReplicaScheduler(pygame.sprite.Sprite):
    """Manages spawning animation replicas at fixed intervals."""
    
    def __init__(self, sprite_groups, sprite, x, y, ani, idx, num_replicas, replica_delay_frames, follow_self=True):
        """
        Args:
            sprite_groups: The sprite groups dict
            x, y, ani, idx: Animation spawn parameters
            num_replicas: Number of additional replicas to spawn
            replica_delay_frames: Frames between each replica spawn
        """
        pygame.sprite.Sprite.__init__(self)
        self.sprite_groups = sprite_groups
        self.sprite = sprite
        self.x = x
        self.y = y
        self.ani = ani
        self.idx = idx
        self.replicas_remaining = num_replicas
        self.replica_delay = replica_delay_frames
        self.frame_counter = 0
        self.follow_self = follow_self
    
    def update(self):
        """Called every frame. Returns True if still spawning, False when done."""
        if self.replicas_remaining <= 0:
            self.kill()  # Remove from any tracking group
            return False
        
        self.frame_counter += 1
        if self.frame_counter >= self.replica_delay:
            if self.follow_self and self.sprite:
                self.x = self.sprite.rect.centerx
                self.y = self.sprite.rect.bottom
            self.sprite_groups['animation'].add(
                Animation(self.x, self.y, self.ani, self.idx)
            )
            self.replicas_remaining -= 1
            self.frame_counter = 0
        
        return True