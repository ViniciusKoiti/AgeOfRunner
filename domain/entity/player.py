from domain.entity.game_object import GameObject
from domain.physics.vector2D import Vector2D
from ports.event_port import EventPort
from ports.physics_port import PhysicsPort


class Player(GameObject):
    def __init__(self, physics: PhysicsPort, position: Vector2D):
        super().__init__(
            physics=physics,
            position=position,
            size=(32, 32),
            mass=1.0  # massa normal para objeto dinâmico
        )
        self.move_force = 1000.0
        self.jump_force = 2000.0
        
    def update(self, delta_time: float):
        super().update(delta_time)

        
        if self.is_grounded:
            self.can_jump = True
            
            current_vel = self.velocity
            friction_factor = 1  # Ajuste conforme necessário
            self.velocity = Vector2D(current_vel.x * friction_factor, current_vel.y)
            
            # Animações
            if abs(self.velocity.x) > 10:
                self.current_animation = "run"
            else:
                self.current_animation = "idle"
        else:
            # Lógica no ar
            if self.velocity.y < 0:
                self.current_animation = "jump"
            else:
                self.current_animation = "fall"
    
    def move_right(self):
        self.apply_force(Vector2D(self.move_force, 0))
        
    def move_left(self):
        self.apply_force(Vector2D(-self.move_force, 0))
        
    def jump(self):

        if(self.is_grounded):
   
            self.apply_force(Vector2D(0, -self.jump_force))

    def handle_input(self, event_handler: EventPort):
        if event_handler.is_key_pressed("left"):
            self.move_left()
        elif event_handler.is_key_pressed("right"):
            self.move_right()
        if event_handler.is_key_pressed("jump"):
            self.jump()