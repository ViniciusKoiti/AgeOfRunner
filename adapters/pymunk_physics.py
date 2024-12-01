import logging
from typing import Dict, Set, Tuple
import pymunk
from domain.physics.vector2D import Vector2D
from ports.physics_port import PhysicsPort

from pymunk.vec2d import Vec2d

logging.basicConfig(level=logging.DEBUG)

class PymunkPhysicsAdapter(PhysicsPort):
    def __init__(self, gravity: Vector2D = Vector2D(0, 9.81)):
        logging.debug("Inicializando PymunkPhysicsAdapter com gravidade: %s", gravity)
        self.space = pymunk.Space()
        self.space.gravity = (gravity.x, gravity.y)
        self.default_gravity = gravity
        self.gravity_multiplier = 1
        
        self.space.iterations = 20
        
        self.bodies: Dict[int, pymunk.Body] = {}
        self.shapes: Dict[int, pymunk.Shape] = {}
        self.next_id = 0
        
        self.CATEGORY_DYNAMIC = 0b001
        self.CATEGORY_GROUND = 0b010
        self.CATEGORY_PLATFORM = 0b100

        self.grounded_bodies: Set[int] = set()
        
        self._setup_collision_handlers()
        
        # Debug flags
        self.debug_collisions = True

    def flip_gravity(self):
        """Inverte a direção da gravidade"""
        self.gravity_multiplier *= -1
        self.space.gravity = (
            self.default_gravity.x,
            self.default_gravity.y * self.gravity_multiplier
        )
        logging.debug(f"Gravidade invertida: {self.space.gravity}")

    def apply_force(self, object_id: int, force: Vector2D) -> None:
        if object_id in self.bodies:
            body = self.bodies[object_id]
            body.apply_force_at_local_point((force.x, force.y), (0, 0))

    def set_velocity(self, object_id: int, velocity: Vector2D) -> None:
        if object_id in self.bodies:
            body = self.bodies[object_id]
            max_velocity = 400
            vx = max(min(velocity.x, max_velocity), -max_velocity)
            vy = max(min(velocity.y, max_velocity), -max_velocity)
            body.velocity = (vx, vy)

    def get_velocity(self, object_id: int) -> Vector2D:
        if object_id in self.bodies:
            body = self.bodies[object_id]
            return Vector2D(body.velocity.x, body.velocity.y)
        return Vector2D(0, 0)

    def get_position(self, object_id: int) -> Vector2D:
        if object_id in self.bodies:
            body = self.bodies[object_id]
            return Vector2D(body.position.x, body.position.y)
        return Vector2D(0, 0)

    def set_position(self, object_id: int, position: Vector2D) -> None:
        if object_id in self.bodies:
            body = self.bodies[object_id]
            body.position = (position.x, position.y)

    def _setup_collision_handlers(self):
        def begin_collision(arbiter, space, data):
            if self.debug_collisions:
                logging.debug(f"Colisão detectada! Normal: {arbiter.normal}")
                logging.debug(f"Gravity multiplier: {self.gravity_multiplier}")
            
            shapes = arbiter.shapes
            normal = arbiter.normal
            logging.debug("Colisão com o chão detectada!")
            # Identifica as shapes
            dynamic_shape = None
            ground_shape = None
            
            for shape in shapes:
                if shape.collision_type == self.CATEGORY_DYNAMIC:
                    dynamic_shape = shape
                elif shape.collision_type == self.CATEGORY_GROUND:
                    ground_shape = shape
            
            if dynamic_shape and ground_shape:
                is_ground_collision = False
                
                if self.gravity_multiplier > 0:  # Gravidade normal
                    is_ground_collision = normal.y > 0.5
                else:  # Gravidade invertida
                    is_ground_collision = normal.y < -0.5
                
                if is_ground_collision:
                    if self.debug_collisions:
                        logging.debug("Colisão com o chão detectada!")
                    
                    # Encontra o ID do corpo dinâmico
                    for body_id, shape in self.shapes.items():
                        if shape == dynamic_shape:
                            self.grounded_bodies.add(body_id)
                            if self.debug_collisions:
                                logging.debug(f"Objeto {body_id} está no chão")
                            break
                return True

        def separate_collision(arbiter, space, data):
            if self.debug_collisions:
                logging.debug("Separação detectada!")
            
            shapes = arbiter.shapes
            dynamic_shape = None
            
            for shape in shapes:
                if shape.collision_type == self.CATEGORY_DYNAMIC:
                    dynamic_shape = shape
                break
                    
            if dynamic_shape:
                for body_id, shape in self.shapes.items():
                    if shape == dynamic_shape:
                        self.grounded_bodies.discard(body_id)
                        if self.debug_collisions:
                            logging.debug(f"Objeto {body_id} não está mais no chão")
                        break
                return True

        ground_handler = self.space.add_collision_handler(
                self.CATEGORY_DYNAMIC,
                self.CATEGORY_GROUND
            )
        
        ground_handler.begin = begin_collision
         
        ground_handler.separate = separate_collision

        dynamic_handler = self.space.add_collision_handler(
        self.CATEGORY_DYNAMIC,
            self.CATEGORY_DYNAMIC
        )
        dynamic_handler.begin = lambda a, s, d: True

    def create_dynamic_body(self, position: Vector2D, size: Tuple[float, float], mass: float) -> int:
        moment = pymunk.moment_for_box(mass, size)
        body = pymunk.Body(mass, moment)
        body.position = (position.x, position.y)
        
        shape = pymunk.Poly.create_box(body, size)
        shape.collision_type = self.CATEGORY_DYNAMIC
        
        shape.filter = pymunk.ShapeFilter(
            categories=self.CATEGORY_DYNAMIC,
            mask=self.CATEGORY_GROUND | self.CATEGORY_PLATFORM | self.CATEGORY_DYNAMIC
        )
        
        self.space.add(body, shape)
        
        body_id = self.next_id
        self.next_id += 1
        self.bodies[body_id] = body
        self.shapes[body_id] = shape
        
        return body_id

    def create_static_body(self, position: Vector2D, size: Tuple[float, float]) -> int:
        segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        segment_body.position = position.x, position.y

        start_point = Vec2d(0, 0)  # Começa na posição do corpo
        end_point = Vec2d(size[0], 0)  # Estende horizontalmente pelo width especificado
        segment = pymunk.Segment(segment_body, start_point, end_point, size[1]/2)  # usa height/2 como espessura
        segment.friction = 1.0
        segment.collision_type = self.CATEGORY_GROUND        
        segment.filter = pymunk.ShapeFilter(
            categories=self.CATEGORY_GROUND,
            mask=self.CATEGORY_DYNAMIC
        )

        self.space.add(segment_body, segment)
    
        body_id = self.next_id
        self.next_id += 1
        self.bodies[body_id] = segment_body
        self.shapes[body_id] = segment
    
        return body_id
        

    def is_grounded(self, object_id: int) -> bool:
        return object_id in self.grounded_bodies

    def update(self, delta_time: float) -> None:
        steps = max(1, delta_time)
        dt = delta_time / steps
    
        for _ in range(steps):
            for body_id in self.bodies:
                body = self.bodies[body_id]
                if body.body_type == pymunk.Body.DYNAMIC:
                    if abs(body.velocity.y) > 500:
                        body.velocity = (body.velocity.x, 500 if body.velocity.y > 0 else -500)
            
            self.space.step(dt)