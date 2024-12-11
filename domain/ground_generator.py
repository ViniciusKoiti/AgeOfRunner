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
        
        # Configurações de altura
        self.bottom_base_height = 500  # Altura base para plataformas inferiores
        self.top_base_height = 100     # Altura base para plataformas superiores
        self.height_variation = 50      # Variação menor para manter equilíbrio
        
        self.last_bottom_height = self.bottom_base_height
        self.last_top_height = self.top_base_height
        
        # Lista de tuplas (segmento, largura) para cada linha de plataformas
        self.bottom_segments: List[Tuple[GroundSegment, float]] = []
        self.top_segments: List[Tuple[GroundSegment, float]] = []
        
    def generate_initial_platforms(self, num_platforms: int = 5) -> List[GroundSegment]:
        """Gera as plataformas iniciais do jogo em ambas as posições"""
        # Plataformas iniciais garantidas para spawn seguro
        initial_width = 300
        
        # Plataforma inferior inicial
        bottom_platform = GroundSegment(
            physics=self.physics,
            position=Vector2D(0, self.bottom_base_height),
            width=initial_width
        )
        self.bottom_segments.append((bottom_platform, initial_width))
        
        # Plataforma superior inicial
        top_platform = GroundSegment(
            physics=self.physics,
            position=Vector2D(0, self.top_base_height),
            width=initial_width
        )
        self.top_segments.append((top_platform, initial_width))
        
        self.last_platform_end = initial_width
        
        # Gera os próximos pares de plataformas
        for _ in range(num_platforms - 1):
            self.generate_next_platforms()
            
        # Retorna todas as plataformas
        return ([segment for segment, _ in self.bottom_segments] + 
                [segment for segment, _ in self.top_segments])
    
    def generate_next_platforms(self) -> Tuple[GroundSegment, GroundSegment]:
        """Gera um novo par de plataformas (superior e inferior)"""
        # Calcula a distância até o próximo par de plataformas
        gap = randint(self.min_gap, self.max_gap)
        start_x = self.last_platform_end + gap
        
        # Determina o tamanho das plataformas (mesmo tamanho para manter simetria)
        width = randint(self.min_platform_width, self.max_platform_width)
        
        # Calcula as alturas com variações controladas
        bottom_height_change = randint(-self.height_variation, self.height_variation)
        top_height_change = randint(-self.height_variation, self.height_variation)
        
        new_bottom_height = max(400, min(550, self.last_bottom_height + bottom_height_change))
        new_top_height = max(50, min(200, self.last_top_height + top_height_change))
        
        # Cria a plataforma inferior
        bottom_platform = GroundSegment(
            physics=self.physics,
            position=Vector2D(start_x, new_bottom_height),
            width=width
        )
        
        # Cria a plataforma superior
        top_platform = GroundSegment(
            physics=self.physics,
            position=Vector2D(start_x, new_top_height),
            width=width
        )
        
        # Atualiza as variáveis de controle
        self.last_platform_end = start_x + width
        self.last_bottom_height = new_bottom_height
        self.last_top_height = new_top_height
        
        # Armazena as novas plataformas
        self.bottom_segments.append((bottom_platform, width))
        self.top_segments.append((top_platform, width))
        
        return bottom_platform, top_platform
    
    def update(self, player_x: float, view_distance: float = 1000) -> List[GroundSegment]:
        """Atualiza as plataformas baseado na posição do player"""
        # Gera novos pares de plataformas se necessário
        while self.last_platform_end < player_x + view_distance:
            self.generate_next_platforms()
        
        # Remove plataformas antigas que ficaram muito para trás
        self.bottom_segments = [
            (segment, width) for segment, width in self.bottom_segments 
            if segment.position.x + width > player_x - view_distance
        ]
        
        self.top_segments = [
            (segment, width) for segment, width in self.top_segments 
            if segment.position.x + width > player_x - view_distance
        ]
        
        # Retorna todas as plataformas ativas
        return ([segment for segment, _ in self.bottom_segments] + 
                [segment for segment, _ in self.top_segments])
    
    def clear(self):
        """Limpa todas as plataformas geradas"""
        self.bottom_segments.clear()
        self.top_segments.clear()
        self.last_platform_end = 0
        self.last_bottom_height = self.bottom_base_height
        self.last_top_height = self.top_base_height