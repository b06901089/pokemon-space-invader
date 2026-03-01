import pygame
from objects import Animation

class ReplicaScheduler(pygame.sprite.Sprite):
    """Manages spawning animation replicas at fixed intervals."""
    
    def __init__(self, 
                 sprite_groups, 
                 sprite, 
                 x, y, 
                 ani, idx, 
                 num_replicas, replica_delay, spawn_dir, 
                 spawn_ops, 
                 spawn_reset, 
                 get_animation_spawn_location):
        """
        Args:
            sprite_groups: The sprite groups dict
            x, y, ani, idx: Animation spawn parameters
            num_replicas: Number of additional replicas to spawn
            replica_delay: Frames between each replica spawn
        """
        pygame.sprite.Sprite.__init__(self)
        self.sprite_groups = sprite_groups
        self.sprite = sprite
        self.x = x
        self.y = y
        self.ani = ani
        self.idx = idx
        self.replicas_remaining = num_replicas
        self.replica_delay = replica_delay
        self.frame_counter = 0
        self.spawn_dir = spawn_dir
        self.spawn_ops = spawn_ops
        self.spawn_reset = spawn_reset
        self.get_animation_spawn_location = get_animation_spawn_location
    
    def update(self):
        """Called every frame. Returns True if still spawning, False when done."""
        if self.replicas_remaining <= 0:
            self.kill()  # Remove from any tracking group
            return False
        
        self.frame_counter += 1
        if self.frame_counter >= self.replica_delay:
            if self.spawn_reset and self.sprite:
                self.x, self.y = self.get_animation_spawn_location(self.sprite_groups, self.sprite, self.spawn_dir, self.spawn_ops)
            if self.spawn_ops:
                self.sprite_groups['my_ani'].add(Animation(self.x, self.y, self.ani, self.idx, self.spawn_ops))
            else:
                self.sprite_groups['animation'].add(Animation(self.x, self.y, self.ani, self.idx, self.spawn_ops))
            self.replicas_remaining -= 1
            self.frame_counter = 0
        
        return True