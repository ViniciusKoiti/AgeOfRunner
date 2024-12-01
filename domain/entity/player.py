from domain.entity.game_object import GameObject
from domain.physics.vector2D import Vector2D
from ports.event_port import EventPort
from ports.physics_port import PhysicsPort
import time


class Player(GameObject):
    def __init__(self, physics: PhysicsPort, position: Vector2D):
        super().__init__(
            physics=physics,
            position=position,
            size=(32, 32),
            mass=50.0
        )
        self.move_force = 3000.0
        self.jump_force = 2000.0
        self.can_toggle_gravity = True
        self.jump_delay = 0.5  # Meio segundo de delay
        self.jump_timer = 0
        self.can_jump = True
        
    def update(self, delta_time: float):
        super().update(delta_time)

        if not self.can_jump:
            self.jump_timer += delta_time
            if self.jump_timer >= self.jump_delay:
                self.can_jump = True
                self.jump_timer = 0
        
        if self.is_grounded:
            self.can_toggle_gravity = True
            
            current_vel = self.velocity
            self.velocity = Vector2D(current_vel.x, current_vel.y)
            
            if abs(self.velocity.x) > 10:
                self.current_animation = "run"
            else:
                self.current_animation = "idle"
        else:
            if self.velocity.y < 0:
                self.current_animation = "jump"
            else:
                self.current_animation = "fall"
    
    def move_right(self):
        self.apply_force(Vector2D(self.move_force, 0))
        
    def move_left(self):
        self.apply_force(Vector2D(-self.move_force, 0))
        
    def jump(self):
        if isinstance(self.physics, PhysicsPort):
            if(self.is_grounded and self.can_jump):
                self.physics.flip_gravity()
                self.can_toggle_gravity = False
                self.can_jump = False
                self.can_toggle_gravity = False  

    def handle_input(self, event_handler: EventPort):
        if event_handler.is_key_pressed("left"):
            self.move_left()
        elif event_handler.is_key_pressed("right"):
            self.move_right()
        if event_handler.is_key_pressed("jump"):
            self.jump()

