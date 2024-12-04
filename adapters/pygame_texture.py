from typing import Tuple
import pygame
from ports.texture_port import TexturePort

class PygameTexture(TexturePort):
    def load_texture(self, path: str) -> pygame.Surface:
        try:
            return pygame.image.load(path)
        except Exception as e:
            print(f"Erro ao carregar textura: {e}")
            return None
            
    def get_sprite_from_sheet(self, 
                           texture: pygame.Surface, 
                           rect: Tuple[int, int, int, int]) -> pygame.Surface:
        frame = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        frame.blit(texture, (0, 0), rect)
        return frame
    
    def flip_sprite(self, sprite: pygame.Surface, 
                   flip_x: bool, flip_y: bool) -> pygame.Surface:
        return pygame.transform.flip(sprite, flip_x, flip_y)