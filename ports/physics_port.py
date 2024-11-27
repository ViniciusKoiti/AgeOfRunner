from abc import ABC, abstractmethod
from typing import Tuple

from domain.physics.vector2D import Vector2D


class PhysicsPort(ABC):
    @abstractmethod
    def apply_force(self, object_id: int, force: Vector2D) -> None:
        """Aplica uma força a um objeto específico"""
        pass
    
    @abstractmethod
    def set_velocity(self, object_id: int, velocity: Vector2D) -> None:
        """Define a velocidade de um objeto"""
        pass
    
    @abstractmethod
    def get_velocity(self, object_id: int) -> Vector2D:
        """Obtém a velocidade atual de um objeto"""
        pass
    
    @abstractmethod
    def create_dynamic_body(self, position: Vector2D, size: Tuple[float, float], mass: float) -> int:
        """Cria um corpo dinâmico e retorna seu ID"""
        pass
    
    @abstractmethod
    def create_static_body(self, position: Vector2D, size: Tuple[float, float]) -> int:
        """Cria um corpo estático e retorna seu ID"""
        pass
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Atualiza a simulação física"""
        pass
    
    @abstractmethod
    def get_position(self, object_id: int) -> Vector2D:
        """Obtém a posição atual de um objeto"""
        pass
    
    @abstractmethod
    def set_position(self, object_id: int, position: Vector2D) -> None:
        """Define a posição de um objeto"""
        pass
    
    @abstractmethod
    def is_grounded(self, object_id: int) -> bool:
        """Verifica se um objeto está no chão"""
        pass

    def flip_gravity(self) -> None:
        pass