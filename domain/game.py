from typing import Dict, List
from domain.entity.camera import Camera
from domain.entity.ground_segment import GroundSegment
from domain.menu import Menu
from domain.entity.player import Player
from domain.entity.game_object import GameObject
from domain.game_state import GameState
from domain.physics.vector2D import Vector2D
from ports.clock_port import ClockPort
from ports.event_port import EventPort
from ports.renderer_port import RendererPort
from ports.physics_port import PhysicsPort
from ports.texture_port import TexturePort
import json
import os

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
        self.score = 0
        self.player_name = ""
        self.waiting_for_name = False
        self.furthest_right = None
        self.player = None
        self.high_scores = self.load_scores()
        
    def load_scores(self) -> List[Dict[str, any]]:
        if not os.path.exists(SCORES_FILE):
            return []
        try:
            with open(SCORES_FILE, 'r') as f:
                return json.loads(f.read())
        except:
            return []
        
    def save_score(self, name: str, score: int):
        scores = self.load_scores()
        scores.append({"name": name, "score": score})
        scores.sort(key=lambda x: x["score"], reverse=True)
        scores = scores[:10]
        
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f)
        
        
    def init_game_objects(self):
        self.player = Player(
            physics=self.physics,
            position=Vector2D(200, 400),
            texture_port=self.texture_port
        )
        self.furthest_right = self.player.position.x  # Inicializa com a posição inicial do player
        
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
            self.waiting_for_name = True  # Ativa a entrada do nome
            self.player_name = ""  # Limpa qualquer nome anterior
            
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
        elif self.state == GameState.GAME_OVER and not self.waiting_for_name:
            if self.event_handler.is_key_pressed("return"):
                self.state = GameState.MENU
                self.game_objects.clear()
                self.player = None
                self.score = 0
                self.furthest_right = None
                
    def update(self, delta_time):
        if self.state == GameState.PLAYING:
            self.physics.update(delta_time)
            if self.player:
                self.camera.follow(self.player.position)
                self.update_score()
                self.check_player_in_bounds()
                
    def start_game(self):
        self.state = GameState.PLAYING
        self.score = 0
        self.furthest_right = None
        self.init_game_objects()
        
    def show_options(self):
        pass
        
    def exit_game(self):
        self.event_handler.quit()
        
    def render(self, delta_time):
        self.renderer.clear()
        
        if self.state == GameState.MENU:
            self.menu.render()
            # Renderiza o ranking
            self.renderer.draw_text("High Scores:", 300, 400, (255, 255, 255))
            for i, score in enumerate(self.high_scores[:5]):
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
            self.renderer.draw_text(f"Score: {self.score}", 5, 5, (255, 255, 255))
        elif self.state == GameState.GAME_OVER:
            self.renderer.draw_text("Game Over!", 300, 250, (255, 0, 0))
            self.renderer.draw_text(f"Final Score: {self.score}", 280, 300, (255, 255, 255))
            if self.waiting_for_name:
                self.renderer.draw_text("Enter your name:", 300, 350, (255, 255, 255))
                self.renderer.draw_text(f"{self.player_name}_", 300, 400, (255, 255, 255))
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
        if not self.player:
            return
            
        current_x = self.player.position.x
        
        if self.furthest_right is None:
            self.furthest_right = current_x
            return
            
        if current_x > self.furthest_right:
            points = int(current_x - self.furthest_right)
            self.score += points
            self.furthest_right = current_x
            
    def process_text_input(self, char: str, is_backspace: bool, is_return: bool):
        if not self.waiting_for_name:
            return
            
        if is_return and len(self.player_name.strip()) > 0:
            self.save_score(self.player_name, self.score)
            self.waiting_for_name = False
            self.player_name = ""
            self.state = GameState.MENU
            self.high_scores = self.load_scores()  # Recarrega as pontuações
            self.game_objects.clear()
            self.player = None
            self.score = 0
            self.furthest_right = None
        elif is_backspace:
            self.player_name = self.player_name[:-1]
        elif len(self.player_name) < MAX_NAME_LENGTH and char.isprintable():
            self.player_name += char 