import pygame
from ports.clock_port import ClockPort

class PygameClock(ClockPort):
    def __init__(self, target_fps: int = 60):
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps
        self.delta_time = 0
        
    def get_delta_time(self) -> float:
        return self.delta_time
        
    def update(self):
        self.delta_time = self.clock.tick(self.target_fps) / 1000.0