from typing import override
import pygame
from ports.event_port import EventPort

class PygameEvent(EventPort):
    def __init__(self):
       self.key_map = {
           "jump": pygame.K_UP,
            "down": pygame.K_DOWN,
           "left": pygame.K_LEFT,
           "right": pygame.K_RIGHT,
           "jump": pygame.K_SPACE,
            "return": pygame.K_BACKSPACE,
       }
       self.current_text_input = ("", False, False)

    @override   
    def is_key_pressed(self, key: str) -> bool:
       keys = pygame.key.get_pressed()
       return keys[self.key_map[key]]
    
    @override   
    def poll_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.current_text_input = ("", True, False)
                elif event.key == pygame.K_RETURN:
                    self.current_text_input = ("", False, True)
                elif event.unicode:
                    self.current_text_input = (event.unicode, False, False)
        return True
    
    @override   
    def quit(self) -> None:
        pygame.quit()
        
    @override
    def get_text_input(self) -> tuple[str, bool, bool]:
        return self.current_text_input

  