from typing import List, Tuple
from domain.physics.vector2D import Vector2D
from ports.physics_port import PhysicsPort
from ports.renderer_port import RendererPort

class GameObject:
    def __init__(self, 
                 physics: PhysicsPort,
                 position: Vector2D, 
                 size: Tuple[int, int], 
                 mass: float = 1.0,
                 sprite_path: str = None):
        self.size = size
        self.sprite = None

        if mass == float('inf'):
            self.body_id = physics.create_static_body(position, size)
        else:
            self.body_id = physics.create_dynamic_body(position, size, mass)
        self.physics = physics
        
    @property
    def position(self) -> Vector2D:
        return self.physics.get_position(self.body_id)
    
    @position.setter
    def position(self, value: Vector2D):
        self.physics.set_position(self.body_id, value)
        
    @property
    def velocity(self) -> Vector2D:
        return self.physics.get_velocity(self.body_id)
    
    @velocity.setter
    def velocity(self, value: Vector2D):
        self.physics.set_velocity(self.body_id, value)
        
    def apply_force(self, force: Vector2D):
        self.physics.apply_force(self.body_id, force)
        
    @property
    def is_grounded(self) -> bool:
        return self.physics.is_grounded(self.body_id)
    
    def update(self, delta_time: float):
        pass
        
    def render(self, renderer: RendererPort):
        if self.sprite:
            renderer.draw_sprite(self.sprite, self.position)
        else:
            renderer.draw_rect(self.position, self.size, (255, 0, 0))

    def render_at_position(self, renderer: RendererPort, screen_pos: Vector2D):
        if self.sprite:
            renderer.draw_sprite(self.sprite, screen_pos)
        else:
            renderer.draw_rect(screen_pos, self.size, (255, 0, 0))        