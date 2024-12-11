from random import randint
from typing import List, Tuple
from domain.physics.vector2D import Vector2D
from domain.entity.ground_segment import GroundSegment
from ports.physics_port import PhysicsPort

class GroundGenerator:
    def __init__(self, physics: PhysicsPort):
        self.physics = physics
        self.last_platform_end = 0
        self.min_gap = 100
        self.max_gap = 200
        self.min_platform_width = 150
        self.max_platform_width = 300
        self.height_variation = 100
        self.base_height = 500
        self.last_height = self.base_height
        self.generated_segments: List[Tuple[GroundSegment, float]] = []  # Tuple com (segmento, largura)
        
    def generate_initial_platforms(self, num_platforms: int = 5) -> List[GroundSegment]:
        """Gera as plataformas iniciais do jogo"""
        # Primeira plataforma é sempre no mesmo lugar para garantir spawn seguro
        initial_width = 300
        initial_platform = GroundSegment(
            physics=self.physics,
            position=Vector2D(0, self.base_height),
            width=initial_width
        )
        self.generated_segments.append((initial_platform, initial_width))
        self.last_platform_end = initial_width
        self.last_height = self.base_height
        
        # Gera as próximas plataformas
        for _ in range(num_platforms - 1):
            self.generate_next_platform()
            
        return [segment for segment, _ in self.generated_segments]
    
    def generate_next_platform(self) -> GroundSegment:
        """Gera uma nova plataforma baseada na posição da última"""
        # Calcula a distância até a próxima plataforma
        gap = randint(self.min_gap, self.max_gap)
        start_x = self.last_platform_end + gap
        
        # Calcula a altura da nova plataforma
        height_change = randint(-self.height_variation, self.height_variation)
        new_height = max(200, min(800, self.last_height + height_change))
        
        # Determina o tamanho da plataforma
        width = randint(self.min_platform_width, self.max_platform_width)
        
        # Cria a nova plataforma
        platform = GroundSegment(
            physics=self.physics,
            position=Vector2D(start_x, new_height),
            width=width
        )
        
        # Atualiza as variáveis de controle
        self.last_platform_end = start_x + width
        self.last_height = new_height
        self.generated_segments.append((platform, width))
        
        return platform
    
    def update(self, player_x: float, view_distance: float = 1000) -> List[GroundSegment]:
        """
        Atualiza as plataformas baseado na posição do player
        Gera novas quando necessário e remove as muito distantes
        """
        # Gera novas plataformas se o jogador estiver se aproximando do fim
        while self.last_platform_end < player_x + view_distance:
            self.generate_next_platform()
        
        # Remove plataformas antigas que ficaram muito para trás
        self.generated_segments = [
            (segment, width) for segment, width in self.generated_segments 
            if segment.position.x + width > player_x - view_distance
        ]
        
        return [segment for segment, _ in self.generated_segments]
    
    def clear(self):
        """Limpa todas as plataformas geradas"""
        self.generated_segments.clear()
        self.last_platform_end = 0
        self.last_height = self.base_height