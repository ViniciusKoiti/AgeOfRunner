import pygame


from adapters.pygame_clock import PygameClock
from adapters.pygame_event import PygameEvent
from adapters.pygame_renderer import PygameRenderer
from adapters.pymunk_physics import PymunkPhysicsAdapter
from domain.game import Game
from domain.physics.vector2D import Vector2D

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    renderer = PygameRenderer(screen)
    event_handler = PygameEvent()
    clock = PygameClock()
    physics = PymunkPhysicsAdapter(Vector2D(0, 98.1))
    
    game = Game(
        renderer=renderer,
        event_handler=event_handler,
        clock=clock,
        physics=physics
    )
    game.run()

if __name__ == "__main__":
    main()