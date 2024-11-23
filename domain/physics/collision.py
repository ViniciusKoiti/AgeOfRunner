from typing import Tuple, TypeVar

from domain.physics.vector2D import Vector2D


GameObject = TypeVar('GameObject')

class CollisionSystem:
    @staticmethod
    def check_collision(pos1: Vector2D, size1: Tuple[int, int],
                       pos2: Vector2D, size2: Tuple[int, int]) -> Tuple[bool, Vector2D]:
        collision = (
            pos1.x < pos2.x + size2[0] and
            pos1.x + size1[0] > pos2.x and
            pos1.y < pos2.y + size2[1] and
            pos1.y + size1[1] > pos2.y
        )
        
        if not collision:
            return False, Vector2D(0, 0)
            
        overlap_x = min(pos1.x + size1[0], pos2.x + size2[0]) - max(pos1.x, pos2.x)
        overlap_y = min(pos1.y + size1[1], pos2.y + size2[1]) - max(pos1.y, pos2.y)
                   
        if overlap_x < overlap_y:
            direction = 1 if pos1.x < pos2.x else -1
            return True, Vector2D(overlap_x * direction, 0)
        else:
            direction = 1 if pos1.y < pos2.y else -1
            return True, Vector2D(0, overlap_y * direction)