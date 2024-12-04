from domain.entity.game_object import GameObject
from domain.physics.vector2D import Vector2D
from ports.physics_port import PhysicsPort
from ports.renderer_port import RendererPort


class GroundSegment(GameObject):
    def __init__(self, physics: PhysicsPort, position: Vector2D, width: float):
        super().__init__(
            physics=physics,
            position=position,
            size=(width, 32),
            mass=float('inf')  # massa infinita para objeto estático
        )

    def render_at_position(self, renderer: RendererPort, screen_pos: Vector2D, delta_time: float):
        super().render_at_position(renderer, screen_pos, delta_time)
        
        if hasattr(renderer, 'debug_mode') and renderer.debug_mode:
            import pygame  # importa localmente para evitar dependência desnecessária
            if isinstance(renderer, pygame.Surface):
                center_x = screen_pos.x + self.size[0]/2
                center_y = screen_pos.y + self.size[1]/2
                pygame.draw.line(
                    renderer.screen,
                    (255, 255, 0),
                    (center_x, center_y),
                    (center_x, center_y),
                    2
                )