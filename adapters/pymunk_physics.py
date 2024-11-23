from typing import Dict, Set, Tuple
import pymunk
from domain.physics.vector2D import Vector2D
from ports.physics_port import PhysicsPort


class PymunkPhysicsAdapter(PhysicsPort):
    def __init__(self, gravity: Vector2D = Vector2D(0, 9.81)):
        self.space = pymunk.Space()
        self.space.gravity = (gravity.x, gravity.y)
        
        self.bodies: Dict[int, pymunk.Body] = {}
        self.shapes: Dict[int, pymunk.Shape] = {}
        self.next_id = 0
        
        self.CATEGORY_DYNAMIC = 1
        self.CATEGORY_GROUND = 2
        self.CATEGORY_PLATFORM = 4

        self.grounded_bodies: Set[int] = set()
        
        self._setup_collision_handlers()

    def apply_force(self, object_id: int, force: Vector2D) -> None:
        """Aplica uma força a um objeto específico"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            body.apply_force_at_local_point((force.x, force.y), (0, 0))

    def set_velocity(self, object_id: int, velocity: Vector2D) -> None:
        """Define a velocidade de um objeto"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            body.velocity = (velocity.x, velocity.y)

    def get_velocity(self, object_id: int) -> Vector2D:
        """Obtém a velocidade atual de um objeto"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            return Vector2D(body.velocity.x, body.velocity.y)
        return Vector2D(0, 0)

    def get_position(self, object_id: int) -> Vector2D:
        """Obtém a posição atual de um objeto"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            return Vector2D(body.position.x, body.position.y)
        return Vector2D(0, 0)

    def set_position(self, object_id: int, position: Vector2D) -> None:
        """Define a posição de um objeto"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            body.position = (position.x, position.y)

    def _setup_collision_handlers(self):
        def begin_collision(arbiter, space, data):
            # Obtém as formas da colisão
            shapes = arbiter.shapes
            normal = arbiter.normal
            
            # Identifica qual shape é o jogador e qual é o chão
            player_shape = None
            ground_shape = None
            
            for shape in shapes:
                if shape.collision_type == self.CATEGORY_DYNAMIC:
                    player_shape = shape
                elif shape.collision_type == self.CATEGORY_GROUND:
                    ground_shape = shape
            
            if player_shape and ground_shape:
                print(normal.y)
                # Verifica se a colisão é vertical (usando o vetor normal)
                if normal.y < -0.7:  # Colisão vindo de cima
                    # Encontra o ID do corpo do jogador
                    for body_id, shape in self.shapes.items():
                        if shape == player_shape:
                            self.grounded_bodies.add(body_id)
                            break
            return True

        def separate_collision(arbiter, space, data):
            shapes = arbiter.shapes
            player_shape = None
            
            for shape in shapes:
                if shape.collision_type == self.CATEGORY_DYNAMIC:
                    player_shape = shape
                    break
                    
            if player_shape:
                for body_id, shape in self.shapes.items():
                    if shape == player_shape:
                        self.grounded_bodies.discard(body_id)
                        break
            return True

        # Configura o handler entre DYNAMIC e GROUND
        handler = self.space.add_collision_handler(
            self.CATEGORY_DYNAMIC,
            self.CATEGORY_GROUND
        )
        handler.begin = begin_collision
        handler.separate = separate_collision

    def create_dynamic_body(self, position: Vector2D, size: Tuple[float, float], mass: float) -> int:
        moment = pymunk.moment_for_box(mass, size)
        body = pymunk.Body(mass, moment)
        body.position = (position.x, position.y)
        
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.0  # Sem elasticidade para melhor controle
        shape.friction = 1    # Fricção moderada
        shape.collision_type = self.CATEGORY_DYNAMIC
        
        # Configura filtro de colisão
        shape.filter = pymunk.ShapeFilter(
            categories=self.CATEGORY_DYNAMIC,
            mask=self.CATEGORY_GROUND | self.CATEGORY_PLATFORM
        )
        self.space.add(body, shape)
        
        body_id = self.next_id
        self.next_id += 1
        self.bodies[body_id] = body
        self.shapes[body_id] = shape
        
        return body_id

    def create_static_body(self, position: Vector2D, size: Tuple[float, float]) -> int:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (position.x, position.y)
        
        shape = pymunk.Poly.create_box(body, size)
        shape.friction = 1
        shape.elasticity = 0.0
        shape.collision_type = self.CATEGORY_GROUND
        
        shape.density = 1
        # Configura filtro de colisão
        shape.filter = pymunk.ShapeFilter(
            categories=self.CATEGORY_GROUND,
            mask=self.CATEGORY_DYNAMIC
        )
        
        self.space.add(body, shape)
        
        body_id = self.next_id
        self.next_id += 1
        self.bodies[body_id] = body
        self.shapes[body_id] = shape
        
        return body_id

    def is_grounded(self, object_id: int) -> bool:
        return object_id in self.grounded_bodies

    def update(self, delta_time: float) -> None:
        fixed_dt = 1/60.0
        steps = max(1, int(delta_time / fixed_dt))
        
        for _ in range(steps):
            self.space.step(fixed_dt)