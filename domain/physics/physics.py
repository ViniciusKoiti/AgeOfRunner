from typing import List
from ..physics.vector2D import Vector2D
from .collision import CollisionSystem

class Physics:
    def __init__(self, gravity: Vector2D, mass: float):
        self.gravity = gravity
        self.mass = mass
        self.velocity = Vector2D(0, 0)
        self.acceleration = Vector2D(0, 0)
        
    def apply_force(self, force: Vector2D):
        self.acceleration = Vector2D(
            force.x / self.mass + self.gravity.x,
            force.y / self.mass + self.gravity.y
        )
    
    def update(self, delta_time: float, objects: List['GameObject']):

        for obj in objects:
            if obj.physics.mass != float('inf'):
                obj.physics.velocity.y += self.gravity.y * delta_time
                obj.position.x += obj.physics.velocity.x * delta_time
                obj.position.y += obj.physics.velocity.y * delta_time
                
        for i, obj1 in enumerate(objects):
            for obj2 in objects[i+1:]:
                collision = CollisionSystem.check_collision(
                    obj1.position, obj1.size,
                    obj2.position, obj2.size
                )
                if collision[0]:
                    self.handle_collision(obj1, obj2, collision[1])

    def handle_collision(self, obj1: 'GameObject', obj2: 'GameObject', penetration: Vector2D):
        if obj1.physics.mass == float('inf') or obj2.physics.mass == float('inf'):
            if obj1.physics.mass == float('inf'):
                self.resolve_static_collision(obj2, penetration)
            else:
                self.resolve_static_collision(obj1, Vector2D(-penetration.x, -penetration.y))
            return
            
                
        total_mass = obj1.physics.mass + obj2.physics.mass
        obj1_ratio = obj2.physics.mass / total_mass
        obj2_ratio = obj1.physics.mass / total_mass
        
        # Resolve penetration
        obj1.position.x -= penetration.x * obj1_ratio
        obj1.position.y -= penetration.y * obj1_ratio
        obj2.position.x += penetration.x * obj2_ratio
        obj2.position.y += penetration.y * obj2_ratio
        
        # Update velocities
        temp_vel = obj1.physics.velocity
        obj1.physics.velocity = obj2.physics.velocity * obj1_ratio
        obj2.physics.velocity = temp_vel * obj2_ratio
        
    def resolve_static_collision(self, obj: 'GameObject', penetration: Vector2D):
        if abs(penetration.y) > abs(penetration.x):
            obj.position.y -= penetration.y
            obj.physics.velocity.y = 0
        if penetration.y < 0:
            obj.is_grounded = True
        else:
            obj.position.x -= penetration.x
            obj.physics.velocity.x = 0