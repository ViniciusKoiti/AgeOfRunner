from typing import List
from domain.entity.game_object import GameObject
from domain.entity.ground_segment import GroundSegment
from domain.entity.player import Player
from domain.ground_generator import GroundGenerator
from domain.physics.vector2D import Vector2D
from ports.physics_port import PhysicsPort
from ports.texture_port import TexturePort


class GameObjectManager:
    def __init__(self, physics: PhysicsPort, texture_port: TexturePort):
        self.physics = physics
        self.texture_port = texture_port
        self.game_objects: List[GameObject] = []
        self.player = None
        self.ground_generator = GroundGenerator(physics)
        
    def initialize_objects(self):
        self.player = Player(
            physics=self.physics,
            position=Vector2D(200, 400),
            texture_port=self.texture_port
        )
        
        ground_segments = self.ground_generator.generate_initial_platforms()
        
        self.game_objects = [self.player] + ground_segments
        
        return self.player.position
        
    def update(self, delta_time: float):
        if self.player:
            current_segments = self.ground_generator.update(self.player.position.x)
            
            self.game_objects = [self.player] + current_segments
            
        for obj in self.game_objects:
            obj.update(delta_time)
            
    def clear(self):
        self.game_objects.clear()
        self.player = None
        self.ground_generator.clear()  # Limpa as plataformas geradas
        
    def get_player(self) -> Player:
        return self.player
        
    def get_objects(self) -> List[GameObject]:
        return self.game_objects