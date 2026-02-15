import pygame
from .constant import DEFAULT_VOLUME

class SoundManager:
    def __init__(self, default_volume=DEFAULT_VOLUME):
        self.sounds = {}
        self.default_volume = default_volume

    def load(self, name, filename):
        path = filename
        try:
            s = pygame.mixer.Sound(str(path))
            s.set_volume(self.default_volume)
            self.sounds[name] = s
        except Exception as e:
            print(f"Warning: failed to load sound {path}: {e}")
            self.sounds[name] = None

    def get(self, name):
        return self.sounds.get(name)

    def play(self, name, loops=0, maxtime=0, fade_ms=0):
        s = self.get(name)
        if s is not None:
            s.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)