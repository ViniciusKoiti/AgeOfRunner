class MenuItem:
    def __init__(self, text: str, action: callable):
        self.text = text
        self.action = action
        self.selected = False