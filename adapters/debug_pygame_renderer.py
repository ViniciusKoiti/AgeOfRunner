from typing import Tuple, override
import pygame
from domain.physics.vector2D import Vector2D
from ports.renderer_port import RendererPort

class DebugPygameRenderer(RendererPort):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.debug_mode = True

    @override    
    def draw_rect(self, position: Vector2D, size: Tuple[int, int], color: Tuple[int, int, int]):
        pygame.draw.rect(self.screen, color, (position.x, position.y, size[0], size[1]))
        
        if self.debug_mode:
            pygame.draw.rect(self.screen, (0, 255, 0), (position.x, position.y, size[0], size[1]), 1)
            
            center_x = position.x + size[0]/2
            center_y = position.y + size[1]/2
            pygame.draw.circle(self.screen, (255, 0, 0), (int(center_x), int(center_y)), 2)
            
            pos_text = f"({int(position.x)},{int(position.y)})"
            size_text = f"{int(size[0])}x{int(size[1])}"
            text_surface = self.font.render(pos_text, True, (255, 255, 0))
            size_surface = self.font.render(size_text, True, (255, 255, 0))
            self.screen.blit(text_surface, (position.x, position.y - 20))
            self.screen.blit(size_surface, (position.x, position.y - 40))

    @override    
    def draw_sprite(self, sprite, position: Vector2D):
        self.screen.blit(sprite, (position.x, position.y))
        if self.debug_mode and sprite:
            pygame.draw.rect(self.screen, (0, 255, 0), 
                           (position.x, position.y, sprite.get_width(), sprite.get_height()), 1)

    @override  
    def clear(self):
        self.screen.fill((0, 0, 0))  # Preenche com preto

    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int]):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
       
    def present(self):
        pygame.display.flip()