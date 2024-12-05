from domain.animation.animation_controller import AnimationController
from domain.entity.game_object import GameObject
from domain.physics.vector2D import Vector2D
from ports.event_port import EventPort
from ports.physics_port import PhysicsPort
import time

from ports.texture_port import TexturePort


class Player(GameObject):
    def __init__(self, physics: PhysicsPort, position: Vector2D, texture_port: TexturePort):
        super().__init__(
            physics=physics,
            position=position,
            size=(32, 32),
            mass=50.0,
        )
        

        self.move_force = 3000.0
        self.jump_force = 2000.0
        self.can_toggle_gravity = True
        self.jump_delay = 0.5 
        self.jump_timer = 0
        self.gravity_inverted = False
        self.movement_threshold = 10 
        self.animator = AnimationController(texture_port)
        self.setup_animations()
        
    def update(self, delta_time: float):
        super().update(delta_time)
        if not self.can_toggle_gravity:
            self.jump_timer += delta_time
            if self.jump_timer >= self.jump_delay:
                self.can_toggle_gravity = True
                self.jump_timer = 0
        if self.velocity.x > 0:
            self.animator.facing_right = True
        elif self.velocity.x < 0:
            self.animator.facing_right = False

        if self.is_grounded:
            if abs(self.velocity.x) > 10:
                self.set_animation("run")
            else:
                self.set_animation("idle")
        else:
            if self.velocity.y < 0:
                self.set_animation("jump")
            else:
                self.set_animation("fall")
        
    def setup_animations(self):
        frame_data = {
            "idle": [(0, 0, 32, 32)],  # Apenas um frame para idle
            "run": [
                (0, 0, 32, 32),    # Frame 1 da corrida
                (32, 0, 32, 32),   # Frame 2 da corrida
                (64, 0, 32, 32),   # Frame 3 da corrida
                (96, 0, 32, 32)    # Frame 4 da corrida
            ],
            "jump": [(0, 32, 32, 32)]  # Frame do pulo
        }
        
        frame_times = {
            "idle": 0.1,
            "run": 0.08,
            "jump": 0.1
        }
        
        try:
            self.animator.load_animations(
                "domain/animation/assets/personagem.png",
                frame_data,
                frame_times
            )
        except Exception as e:
            print(f"Erro ao carregar animações: {e}")
    
    def move_right(self):
        self.apply_force(Vector2D(self.move_force, 0))
        
    def move_left(self):
        self.apply_force(Vector2D(-self.move_force, 0))
        
    def jump(self):
        if isinstance(self.physics, PhysicsPort):
            if(self.is_grounded and self.can_toggle_gravity):
                self.gravity_inverted = not self.gravity_inverted  # Inverte o estado da gravidade
                self.animator.gravity_inverted = self.gravity_inverted  # Atualiza o animator
                self.physics.flip_gravity()
                self.can_toggle_gravity = False

    def handle_input(self, event_handler: EventPort):
        if event_handler.is_key_pressed("left"):
            self.move_left()
        elif event_handler.is_key_pressed("right"):
            self.move_right()
        if event_handler.is_key_pressed("jump"):
            self.jump()

    

