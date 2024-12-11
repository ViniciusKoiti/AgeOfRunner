from domain.entity.camera import Camera
from domain.game_object import GameObjectManager
from domain.game_renderer import GameRenderer
from domain.game_state import GameState
from domain.game_state_manager import GameStateManager
from domain.input_handler import InputHandler
from domain.menu import Menu
from domain.name_input_manager import NameInputManager
from domain.score_manager import ScoreManager
from domain.score_tracker import ScoreTracker
from ports.clock_port import ClockPort
from ports.event_port import EventPort
from ports.physics_port import PhysicsPort
from ports.renderer_port import RendererPort
from ports.texture_port import TexturePort
import pygame

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
        self.clock = clock
        self.physics = physics
        self.renderer = renderer
        self.event_handler = event_handler
        # Gerenciadores
        self.state_manager = GameStateManager()
        self.object_manager = GameObjectManager(physics, texture_port)
        self.input_handler = InputHandler(event_handler)
        self.game_renderer = GameRenderer(renderer)
        self.score_manager = ScoreManager(SCORES_FILE)
        self.name_input = NameInputManager(MAX_NAME_LENGTH)
        self.score_tracker = ScoreTracker()

        
        
        # Componentes do jogo
        self.camera = Camera(800, 600, WORLD_BOUNDS)
        self.menu = self.create_menu()
        self.pause_menu = self.create_pause_menu()
        

    def create_menu(self) -> Menu:
        menu = Menu(self.renderer)
        menu.add_item("Start Game", self.start_game)
        menu.add_item("Options", self.show_options)
        menu.add_item("Exit", self.exit_game)
        return menu
    
    
    def resume_game(self):
        """Resume the game from pause state"""
        self.state_manager.change_state(GameState.PLAYING)

    def restart_game(self):
        """Restart the game"""
        self.reset_game()
        self.start_game()

    def exit_to_menu(self):
        """Exit to main menu"""
        self.reset_game()
        self.state_manager.change_state(GameState.MENU)
    
    
    def create_pause_menu(self) -> Menu:
        pause_menu = Menu(self.renderer)
        pause_menu.add_item("Resume", self.resume_game)
        pause_menu.add_item("Restart", self.restart_game)
        pause_menu.add_item("Exit to Menu", self.exit_to_menu)
        return pause_menu

    def toggle_pause(self):
        current_state = self.state_manager.get_current_state()
        if current_state == GameState.PLAYING:
            self.state_manager.change_state(GameState.PAUSED)
        elif current_state == GameState.PAUSED:
            self.state_manager.change_state(GameState.PLAYING)

    def start_game(self):
        self.state_manager.change_state(GameState.PLAYING)
        self.score_tracker.reset()
        initial_position = self.object_manager.initialize_objects()
        self.score_tracker.initialize_position(initial_position)
        pygame.mixer.music.load('domain/animation/assets/Sound/music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    def check_player_in_bounds(self):
        player = self.object_manager.get_player()
        if player and self.camera.is_in_death_zone(player.position):
            self.state_manager.change_state(GameState.GAME_OVER)
            self.name_input.start_input()

    def handle_input(self):
        current_state = self.state_manager.get_current_state()
        
        if current_state == GameState.MENU:
            self.input_handler.handle_menu_input(self.menu)
            
        elif current_state == GameState.PLAYING:
            self.input_handler.handle_game_input(self.object_manager.get_player())
            if self.input_handler.check_pause_input():  # Allow unpausing
                self.toggle_pause()
            
        elif current_state == GameState.PAUSED:
            self.input_handler.handle_menu_input(self.pause_menu)
            if self.input_handler.check_pause_input():  # Allow unpausing
                self.toggle_pause()
            
        elif current_state == GameState.GAME_OVER and not self.name_input.active:
            if self.input_handler.handle_game_over_input(self.name_input):
                self.state_manager.change_state(GameState.MENU)
                self.reset_game()

    def update(self, delta_time):
        if self.state_manager.is_playing():
            self.physics.update(delta_time)
            self.object_manager.update(delta_time)
            
            player = self.object_manager.get_player()
            if player:
                self.camera.follow(player.position)
                self.score_tracker.update_score(player.position)
                self.check_player_in_bounds()

    def render(self, delta_time):
        current_state = self.state_manager.get_current_state()
    
        if current_state == GameState.MENU:
            self.game_renderer.render_menu(self.menu, self.score_manager.get_top_scores(5))
        
        elif current_state == GameState.PLAYING:
            self.game_renderer.render_game(
            self.object_manager.get_objects(),
            self.camera,
            self.score_tracker.get_score(),
            delta_time
        )
        
        elif current_state == GameState.PAUSED:
            self.game_renderer.render_game(
            self.object_manager.get_objects(),
            self.camera,
            self.score_tracker.get_score(),
            delta_time
        )
            self.game_renderer.render_pause_menu(self.pause_menu)
        
        elif current_state == GameState.GAME_OVER:
            self.game_renderer.render_game_over(
            self.score_tracker.get_score(),
            self.name_input
        )
        
        self.game_renderer.present()

    def process_text_input(self, char: str, is_backspace: bool, is_return: bool):
        if self.name_input.process_input(char, is_backspace, is_return):
            self.score_manager.save_score(
                self.name_input.get_name(), 
                self.score_tracker.get_score()
            )
            self.name_input.stop_input()
            self.state_manager.change_state(GameState.MENU)
            self.score_manager.reload_scores()
            self.reset_game()

   
    def reset_game(self):
        """Reset completo do estado do jogo"""
        self.object_manager.clear()
        self.score_tracker.reset()
        if hasattr(self.physics, 'space'):
            self.physics.space.remove(*self.physics.space.bodies)
            self.physics.space.remove(*self.physics.space.shapes)
        self.physics.bodies.clear()
        self.physics.shapes.clear()
        self.physics.next_id = 0
        self.physics.grounded_bodies.clear()


    def run(self):
        running = True
        while running:
            delta_time = self.clock.get_delta_time()
            running = self.event_handler.poll_events()
            
            if self.state_manager.is_game_over():
                char, is_backspace, is_return = self.input_handler.get_text_input()
                self.process_text_input(char, is_backspace, is_return)
                
            self.handle_input()
            self.update(delta_time)
            self.render(delta_time)
            self.clock.update()
            
        if hasattr(self.physics, 'cleanup'):
            self.physics.cleanup()
        self.event_handler.quit()

    def show_options(self):
        pass

    def exit_game(self):
        self.event_handler.quit()