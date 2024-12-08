from domain.game_state import GameState


class GameStateManager:
    def __init__(self):
        self.state = GameState.MENU
        
    def change_state(self, new_state: GameState):
        self.state = new_state
        
    def is_menu(self) -> bool:
        return self.state == GameState.MENU
        
    def is_playing(self) -> bool:
        return self.state == GameState.PLAYING
        
    def is_game_over(self) -> bool:
        return self.state == GameState.GAME_OVER
        
    def get_current_state(self) -> GameState:
        return self.state
    
    