from typing import Any, Dict, List, Tuple
from domain.animation.animation import Animation
from ports.texture_port import TexturePort


class AnimationController:
    def __init__(self, texture_port: TexturePort):
        self.texture_port = texture_port
        self.animations: Dict[str, Animation] = {}
        self.current_animation = "idle"
        self.facing_right = True
        
    def load_animations(self, sprite_sheet_path: str, 
                       frame_data: Dict[str, List[Tuple[int, int, int, int]]], 
                       frame_times: Dict[str, float]):
        sprite_sheet = self.texture_port.load_texture(sprite_sheet_path)
        
        for anim_name, frames in frame_data.items():
            sprite_frames = []
            for frame_rect in frames:
                sprite = self.texture_port.get_sprite_from_sheet(sprite_sheet, frame_rect)
                sprite_frames.append(sprite)
            
            self.animations[anim_name] = Animation(
                frames=sprite_frames,
                frame_time=frame_times[anim_name]
            )
    
    def set_animation(self, animation_name: str):
        if animation_name != self.current_animation and animation_name in self.animations:
            self.current_animation = animation_name
            self.animations[animation_name].current_frame = 0
            self.animations[animation_name].time_accumulated = 0
    
    def update(self, delta_time: float) -> Any:
        if self.current_animation in self.animations:
            sprite = self.animations[self.current_animation].update(delta_time)
            if not self.facing_right:
                sprite = self.texture_port.flip_sprite(sprite, True, False)
            return sprite
        return None