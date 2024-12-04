from typing import Dict, List, Any
from ports.texture_port import TexturePort

class Animation:
    def __init__(self, frames: List[Any], frame_time: float):
        self.frames = frames
        self.frame_time = frame_time
        self.current_frame = 0
        self.time_accumulated = 0
        
    def update(self, delta_time: float) -> Any:
        self.time_accumulated += delta_time
        
        if self.time_accumulated >= self.frame_time:
            self.time_accumulated = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
        return self.frames[self.current_frame]
