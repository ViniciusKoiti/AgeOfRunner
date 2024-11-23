from domain.entity.game_object import GameObject
from domain.physics.vector2D import Vector2D
from ports.physics_port import PhysicsPort


class GroundSegment(GameObject):
    def __init__(self, physics: PhysicsPort, position: Vector2D, width: float):
        super().__init__(
            physics=physics,
            position=position,
            size=(width, 32),
            mass=float('inf')  # massa infinita para objeto estático
        )