from abc import ABC, abstractmethod

class ClockPort(ABC):
    @abstractmethod
    def get_delta_time(self) -> float: pass
    
    @abstractmethod
    def update(self): pass