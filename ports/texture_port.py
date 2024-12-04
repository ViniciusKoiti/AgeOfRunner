from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

class TexturePort(ABC):
    @abstractmethod
    def load_texture(self, path: str) -> Any:
        pass
    
    @abstractmethod
    def get_sprite_from_sheet(self, 
                            texture: Any, 
                            rect: Tuple[int, int, int, int]) -> Any:
        pass
    
    @abstractmethod
    def flip_sprite(self, sprite: Any, flip_x: bool, flip_y: bool) -> Any:
        pass