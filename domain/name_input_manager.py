class NameInputManager:
    def __init__(self, max_length: int = 20):
        self.max_length = max_length
        self.name = ""
        self.active = False
        
    def start_input(self):
        self.active = True
        self.name = ""
        
    def stop_input(self):
        self.active = False
        self.name = ""
        
    def process_input(self, char: str, is_backspace: bool, is_return: bool) -> bool:

        if not self.active:
            return False
            
        if is_return and len(self.name.strip()) > 0:
            return True
        elif is_backspace:
            self.name = self.name[:-1]
        elif len(self.name) < self.max_length and char.isprintable():
            self.name += char
            
        return False
        
    def get_name(self) -> str:
        return self.name