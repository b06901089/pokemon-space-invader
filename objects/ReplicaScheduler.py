import pygame
from objects import Animation

class ReplicaScheduler(pygame.sprite.Sprite):
    """Manages spawning animation replicas at fixed intervals."""
    
    def __init__(self, sprite_groups, x, y, ani, idx, num_replicas, replica_delay_frames):
        """
        Args:
            sprite_groups: The sprite groups dict
            x, y, ani, idx: Animation spawn parameters
            num_replicas: Number of additional replicas to spawn
            replica_delay_frames: Frames between each replica spawn
        """
        pygame.sprite.Sprite.__init__(self)
        self.sprite_groups = sprite_groups
        self.x = x
        self.y = y
        self.ani = ani
        self.idx = idx
        self.replicas_remaining = num_replicas
        self.replica_delay = replica_delay_frames
        self.frame_counter = 0
    
    def update(self):
        """Called every frame. Returns True if still spawning, False when done."""
        if self.replicas_remaining <= 0:
            self.kill()  # Remove from any tracking group
            return False
        
        self.frame_counter += 1
        if self.frame_counter >= self.replica_delay:
            # Time to spawn next replica
            self.sprite_groups['animation'].add(
                Animation(self.x, self.y, self.ani, self.idx)
            )
            self.replicas_remaining -= 1
            self.frame_counter = 0
        
        return True