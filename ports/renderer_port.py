from abc import ABC, abstractmethod
from typing import Tuple
from domain.physics.vector2D import Vector2D


class RendererPort(ABC):
    @abstractmethod
    def draw_rect(self, position: Vector2D, size: Tuple[int, int], color: Tuple[int, int, int]): pass
    
    @abstractmethod
    def draw_sprite(self, sprite, position: Vector2D): pass

    @abstractmethod
    def clear(self): pass

    @abstractmethod
    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int]): pass

    @abstractmethod
    def present(self): pass