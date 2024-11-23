from abc import ABC, abstractmethod

class EventPort(ABC):
    @abstractmethod
    def is_key_pressed(self, key: str) -> bool: pass

    @abstractmethod
    def poll_events(self) -> bool:
        pass
        
    @abstractmethod
    def quit(self): pass