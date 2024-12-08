from typing import Dict, List
from domain.entity.camera import Camera
from domain.entity.ground_segment import GroundSegment
from domain.menu import Menu
from domain.entity.player import Player
from domain.entity.game_object import GameObject
from domain.game_state import GameState
from domain.name_input_manager import NameInputManager
from domain.physics.vector2D import Vector2D
from domain.score_manager import ScoreManager
from domain.score_tracker import ScoreTracker
from ports.clock_port import ClockPort
from ports.event_port import EventPort
from ports.renderer_port import RendererPort
from ports.physics_port import PhysicsPort
from ports.texture_port import TexturePort

WORLD_BOUNDS = (0, 0, 500, 500)
SCORES_FILE = "scores.txt"
MAX_NAME_LENGTH = 20

class Game:
    def __init__(self, 
                 renderer: RendererPort, 
                 event_handler: EventPort, 
                 clock: ClockPort,
                 physics: PhysicsPort,
                 texture_port: TexturePort
                 ):
        self.renderer = renderer
        self.event_handler = event_handler
        self.texture_port = texture_port
        self.clock = clock
        self.physics = physics
        self.state = GameState.MENU
        self.game_objects: List[GameObject] = []
        self.camera = Camera(800, 600, WORLD_BOUNDS)
        self.menu = self.create_menu()
        self.player = None
        
        # Gerenciadores
        self.score_manager = ScoreManager(SCORES_FILE)
        self.name_input = NameInputManager(MAX_NAME_LENGTH)
        self.score_tracker = ScoreTracker()
        
    def init_game_objects(self):
        self.player = Player(
            physics=self.physics,
            position=Vector2D(200, 400),
            texture_port=self.texture_port
        )
        self.score_tracker.initialize_position(self.player.position)
        
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

        self.game_objects.extend([self.player, ground, ground2])
        
    def check_player_in_bounds(self):
        if self.player and self.camera.is_in_death_zone(self.player.position):
            self.state = GameState.GAME_OVER
            self.name_input.start_input()
            
    def create_menu(self) -> Menu:
        menu = Menu(self.renderer)
        menu.add_item("Start Game", self.start_game)
        menu.add_item("Options", self.show_options)
        menu.add_item("Exit", self.exit_game)
        return menu
                
    def handle_input(self):
        if self.state == GameState.MENU:
            if self.event_handler.is_key_pressed("jump"):
                self.menu.select_previous()
            elif self.event_handler.is_key_pressed("down"):
                self.menu.select_next()
            elif self.event_handler.is_key_pressed("return"):
                self.menu.activate_selected()
        elif self.state == GameState.PLAYING:
            if self.player:
                self.player.handle_input(self.event_handler)
        elif self.state == GameState.GAME_OVER and not self.name_input.active:
            if self.event_handler.is_key_pressed("return"):
                self.state = GameState.MENU
                self.reset_game()
                
    def update(self, delta_time):
        if self.state == GameState.PLAYING:
            self.physics.update(delta_time)
            if self.player:
                self.camera.follow(self.player.position)
                self.update_score()
                self.check_player_in_bounds()
                
    def start_game(self):
        self.state = GameState.PLAYING
        self.score_tracker.reset()
        self.init_game_objects()
        
    def show_options(self):
        pass
        
    def exit_game(self):
        self.event_handler.quit()
        
    def render(self, delta_time):
        self.renderer.clear()
        
        if self.state == GameState.MENU:
            self.menu.render()
            self.renderer.draw_text("High Scores:", 300, 400, (255, 255, 255))
            for i, score in enumerate(self.score_manager.get_top_scores(5)):
                self.renderer.draw_text(
                    f"{i+1}. {score['name']}: {score['score']}", 
                    300, 
                    440 + i*30, 
                    (255, 255, 255)
                )
        elif self.state == GameState.PLAYING:
            for obj in self.game_objects:
                if self.camera.is_in_view(obj.position, obj.size[0], obj.size[1]):
                    screen_pos = self.camera.world_to_screen(obj.position)
                    obj.render_at_position(self.renderer, screen_pos, delta_time)
            self.renderer.draw_text(f"Score: {self.score_tracker.get_score()}", 5, 5, (255, 255, 255))
        elif self.state == GameState.GAME_OVER:
            self.renderer.draw_text("Game Over!", 300, 250, (255, 0, 0))
            self.renderer.draw_text(f"Final Score: {self.score_tracker.get_score()}", 280, 300, (255, 255, 255))
            if self.name_input.active:
                self.renderer.draw_text("Enter your name:", 300, 350, (255, 255, 255))
                self.renderer.draw_text(f"{self.name_input.name}_", 300, 400, (255, 255, 255))
                self.renderer.draw_text("Press ENTER to confirm", 250, 450, (255, 255, 255))
            else:
                self.renderer.draw_text("Press BACKSPACE to return to menu", 200, 350, (255, 255, 255))
           
        self.renderer.present()
            
    def run(self):
        running = True
        while running:
            delta_time = self.clock.get_delta_time()
            running = self.event_handler.poll_events()
            if self.state == GameState.GAME_OVER:
                char, is_backspace, is_return = self.event_handler.get_text_input()
                self.process_text_input(char, is_backspace, is_return)
            self.handle_input()
            self.update(delta_time)
            self.render(delta_time)
            self.clock.update()
            
        if hasattr(self.physics, 'cleanup'):
            self.physics.cleanup()
        self.event_handler.quit()
        
    def update_score(self):
        if self.player:
            self.score_tracker.update_score(self.player.position)
            
    def process_text_input(self, char: str, is_backspace: bool, is_return: bool):
        if self.name_input.process_input(char, is_backspace, is_return):
            self.score_manager.save_score(self.name_input.get_name(), 
                                        self.score_tracker.get_score())
            self.name_input.stop_input()
            self.state = GameState.MENU
            self.score_manager.reload_scores()
            self.reset_game()
            
    def reset_game(self):
        self.game_objects.clear()
        self.player = None
        self.score_tracker.reset()