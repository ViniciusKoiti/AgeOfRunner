from domain.physics.vector2D import Vector2D


class ScoreTracker:
    def __init__(self):
        self.score = 0
        self.furthest_right = None
        
    def reset(self):
        self.score = 0
        self.furthest_right = None
        
    def initialize_position(self, position: Vector2D):
        self.furthest_right = position.x
        
    def update_score(self, current_position: Vector2D) -> int:
       
        if self.furthest_right is None:
            self.furthest_right = current_position.x
            return 0
            
        if current_position.x > self.furthest_right:
            points = int(current_position.x - self.furthest_right)
            self.score += points
            self.furthest_right = current_position.x
            return points
            
        return 0
        
    def get_score(self) -> int:
        return self.score