from typing import List
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

WORLD_BOUNDS = (0, 0, 500, 500)

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
        self.physics = physics  # Nova porta de física
        self.state = GameState.MENU
        self.game_objects: List[GameObject] = []
        self.camera = Camera(800, 600, WORLD_BOUNDS)
        self.menu = self.create_menu()
        
    def create_menu(self) -> Menu:
        menu = Menu(self.renderer)
        menu.add_item("Start Game", self.start_game)
        menu.add_item("Options", self.show_options)
        menu.add_item("Exit", self.exit_game)
        return menu
    
    def init_game_objects(self):
        player = Player(
            physics=self.physics,
            position=Vector2D(200, 400),
            texture_port=self.texture_port
        )
        
        ground = GroundSegment(
            physics=self.physics,
            position=Vector2D(0, 550),
            width=300
        )

        ground2 = GroundSegment(
            physics=self.physics,
            position=Vector2D(0, 300),
            width=300
        )

        self.game_objects.extend([player, ground, ground2])
        
        
    def start_game(self):
        self.state = GameState.PLAYING
        self.init_game_objects()
        
    def show_options(self):
        pass
        
    def exit_game(self):
        self.event_handler.quit()
        
    def handle_input(self):
        if self.state == GameState.MENU:
            if self.event_handler.is_key_pressed("jump"):
                self.menu.select_previous()
            elif self.event_handler.is_key_pressed("down"):
                self.menu.select_next()
            elif self.event_handler.is_key_pressed("return"):
                self.menu.activate_selected()
        elif self.state == GameState.PLAYING:
            for obj in self.game_objects:
                if isinstance(obj, Player):
                    obj.handle_input(self.event_handler)
                    break
                
    def update(self, delta_time):
    
       
        for obj in self.game_objects:
            obj.update(delta_time)

        if self.state == GameState.PLAYING:
            self.physics.update(delta_time)
            for obj in self.game_objects:
                if isinstance(obj, Player):
                    self.camera.follow(obj.position)
                    break
        self.renderer.present()    
            
    def render(self, delta_time):
        self.renderer.clear()
        
        if self.state == GameState.MENU:
            self.menu.render()
        elif self.state == GameState.PLAYING:
            for obj in self.game_objects:
                if self.camera.is_in_view(obj.position, obj.size[0], obj.size[1]):
                    screen_pos = self.camera.world_to_screen(obj.position)
                    obj.render_at_position(self.renderer, screen_pos, delta_time)
           
        self.renderer.present()
            
    def run(self):
        running = True
        while running:
            delta_time = self.clock.get_delta_time()
            running = self.event_handler.poll_events()
            self.handle_input()
            self.update(delta_time)
            self.render(delta_time)
            self.clock.update()
            
        if hasattr(self.physics, 'cleanup'):
            self.physics.cleanup()
        self.event_handler.quit()


   

if __name__ == "__main__":
    game = create_game()
    game.run()