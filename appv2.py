import time
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, COLORS
from levels.tutorial_level import TUTORIAL_LEVEL

from aether.core.app import App
from aether.core.input import Input
from aether.ecs.world import World
from aether.render.camera import Camera
from aether.physics.physics import Transform, Collider
from aether.platformer.character import Character
from aether.platformer.components import Params
from aether.platformer.systems import InputSystem, MovementSystem, TileCollisionSystem


def build_platforms(level_data):
    platforms = []
    for row_idx, row in enumerate(level_data):
        for col_idx, cell in enumerate(row):
            if cell == 'X':
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                platforms.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    return platforms


def main():
    app = App(size=(SCREEN_WIDTH, SCREEN_HEIGHT), caption='Elemental (aether) - appv2', fps=60)
    input_mgr = Input({'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_SPACE, 'quit': pygame.K_ESCAPE})
    world = World()
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Build simple tile platforms from tutorial level
    platforms = build_platforms(TUTORIAL_LEVEL)

    # Create player via Character wrapper
    spawn_x, spawn_y = 100, 100
    params = Params(speed=460.0, jump_speed=-800.0)
    player = Character(world, spawn_x, spawn_y, 32, 48, params=params)

    # Systems
    world.add_system(InputSystem(world, input_mgr))
    world.add_system(MovementSystem(world))
    world.add_system(TileCollisionSystem(world, platforms))

    last_time = time.time()
    running = True
    while running and app.running:
        now = time.time()
        dt = now - last_time
        # Clamp dt to avoid physics explosions on slow frames
        if dt > 1.0 / 30.0:
            dt = 1.0 / 30.0
        last_time = now

        app.poll()
        input_mgr.poll()
        app.begin_frame()

        # Update world (systems handle input/movement/collision)
        world.update(dt)

        # Update camera target from player
        tr = player.get(Transform)
        col = player.get(Collider)
        camera.follow(tr.x + col.w / 2, tr.y + col.h / 2, slowness=0.2)

        # Draw level
        for tile in platforms:
            draw_rect = pygame.Rect(tile.x - camera.x, tile.y - camera.y, tile.w, tile.h)
            pygame.draw.rect(app.screen, COLORS['platform'], draw_rect)

        # Draw player
        prect = pygame.Rect(int(tr.x - camera.x), int(tr.y - camera.y), col.w, col.h)
        pygame.draw.rect(app.screen, (240, 240, 255), prect)

        app.end_frame()

    app.quit()


if __name__ == '__main__':
    main()


