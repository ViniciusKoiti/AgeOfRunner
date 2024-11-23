from typing import Tuple, override
import pygame
from domain.physics.vector2D import Vector2D
from ports.renderer_port import RendererPort

class PygameRenderer(RendererPort):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    @override    
    def draw_rect(self, position: Vector2D, size: Tuple[int, int], color: Tuple[int, int, int]):
        pygame.draw.rect(self.screen, color, (position.x, position.y, size[0], size[1]))

    @override    
    def draw_sprite(self, sprite, position: Vector2D):
        self.screen.blit(sprite, (position.x, position.y))

    @override  
    def clear(self):
        self.screen.fill((0, 0, 0))  # Fill with black

    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int]):
       text_surface = self.font.render(text, True, color)
       self.screen.blit(text_surface, (x, y))
       
    def present(self):
       pygame.display.flip()