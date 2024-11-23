from typing import List
from domain.menu_item import MenuItem
from ports import renderer_port


class Menu:
    def __init__(self, renderer: renderer_port):
        self.renderer = renderer
        self.items: List[MenuItem] = []
        self.selected_index = 0
        
    def add_item(self, text: str, action: callable):
        self.items.append(MenuItem(text, action))
        
    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.items)
        
    def select_previous(self):
        self.selected_index = (self.selected_index - 1) % len(self.items)
        
    def activate_selected(self):
        if 0 <= self.selected_index < len(self.items):
            self.items[self.selected_index].action()
            
    def render(self):
        y_offset = 200
        for i, item in enumerate(self.items):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            self.renderer.draw_text(item.text, 300, y_offset + i * 50, color)