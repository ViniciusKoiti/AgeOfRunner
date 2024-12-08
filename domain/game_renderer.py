from typing import Dict, List
from domain.entity.camera import Camera
from domain.entity.game_object import GameObject
from domain.menu import Menu
from domain.name_input_manager import NameInputManager
from domain.physics.vector2D import Vector2D
from ports.renderer_port import RendererPort


class GameRenderer:
    def __init__(self, renderer: RendererPort):
        self.renderer = renderer
        
    def render_menu(self, menu: Menu, high_scores: List[Dict]):
        self.renderer.clear()
        menu.render()
        self.renderer.draw_text("High Scores:", 300, 400, (255, 255, 255))
        for i, score in enumerate(high_scores):
            self.renderer.draw_text(
                f"{i+1}. {score['name']}: {score['score']}", 
                300, 
                440 + i*30, 
                (255, 255, 255)
            )
            
    def render_game(self, game_objects: List[GameObject], camera: Camera, score: int, delta_time: float):
        self.renderer.clear()
        for obj in game_objects:
            if camera.is_in_view(obj.position, obj.size[0], obj.size[1]):
                screen_pos = camera.world_to_screen(obj.position)
                obj.render_at_position(self.renderer, screen_pos, delta_time)
        self.renderer.draw_text(f"Score: {score}", 5, 5, (255, 255, 255))
        
    def render_game_over(self, score: int, name_input_manager: NameInputManager):
        self.renderer.clear()
        self.renderer.draw_text("Game Over!", 300, 250, (255, 0, 0))
        self.renderer.draw_text(f"Final Score: {score}", 280, 300, (255, 255, 255))
        
        if name_input_manager.active:
            self.renderer.draw_text("Enter your name:", 300, 350, (255, 255, 255))
            self.renderer.draw_text(f"{name_input_manager.name}_", 300, 400, (255, 255, 255))
            self.renderer.draw_text("Press ENTER to confirm", 250, 450, (255, 255, 255))
        else:
            self.renderer.draw_text("Press BACKSPACE to return to menu", 200, 350, (255, 255, 255))
            
    def present(self):
        self.renderer.present()
        
    def render_pause_menu(self, pause_menu: Menu):
        overlay_color = (0, 0, 0, 128)  
        self.renderer.draw_rect(
            Vector2D(0, 0),
            (800, 600), 
            overlay_color
        )
    
        self.renderer.draw_text("PAUSED", 350, 150, (255, 255, 255))
    
        pause_menu.render()