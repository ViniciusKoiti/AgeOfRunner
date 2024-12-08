from typing import List
from domain.entity.game_object import GameObject
from domain.entity.ground_segment import GroundSegment
from domain.entity.player import Player
from domain.physics.vector2D import Vector2D
from ports.physics_port import PhysicsPort
from ports.texture_port import TexturePort


class GameObjectManager:
    def __init__(self, physics: PhysicsPort, texture_port: TexturePort):
        self.physics = physics
        self.texture_port = texture_port
        self.game_objects: List[GameObject] = []
        self.player = None
        
    def initialize_objects(self):
        self.player = Player(
            physics=self.physics,
            position=Vector2D(200, 400),
            texture_port=self.texture_port
        )
        
        ground = GroundSegment(
            physics=self.physics,
            position=Vector2D(0, 500),
            width=300
        )

        ground2 = GroundSegment(
            physics=self.physics,
            position=Vector2D(0, 50),
            width=300
        )

        self.game_objects = [self.player, ground, ground2]
        return self.player.position
        
    def update(self, delta_time: float):
        for obj in self.game_objects:
            obj.update(delta_time)
            
    def clear(self):
        self.game_objects.clear()
        self.player = None
        
    def get_player(self) -> Player:
        return self.player
        
    def get_objects(self) -> List[GameObject]:
        return self.game_objects