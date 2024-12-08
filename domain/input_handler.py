from domain.entity.player import Player
from domain.menu import Menu
from domain.name_input_manager import NameInputManager
from ports.event_port import EventPort


class InputHandler:
    def __init__(self, event_handler: EventPort):
        self.event_handler = event_handler
        
    def handle_menu_input(self, menu: Menu):
        if self.event_handler.is_key_pressed("jump"):
            menu.select_previous()
        elif self.event_handler.is_key_pressed("down"):
            menu.select_next()
        elif self.event_handler.is_key_pressed("return"):
            menu.activate_selected()
            
    def handle_game_input(self, player: Player):
        if player:
            player.handle_input(self.event_handler)
            
    def handle_game_over_input(self, name_input: NameInputManager) -> bool:
        if not name_input.active and self.event_handler.is_key_pressed("return"):
            return True
        return False
        
    def get_text_input(self):
        return self.event_handler.get_text_input()