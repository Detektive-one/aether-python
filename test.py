import pygame
import time

from aether.core.app import App
from aether.core.input import Input
from aether.ecs.world import World
from aether.physics.physics import Transform, Kinematics, MovementSystem, Collider


def main():
    app = App(size=(800, 600), caption='Aether Test', fps=60)
    world = World()
    input_mgr = Input()

    # Systems
    world.add_system(MovementSystem(world))

    # Create a simple entity
    player = world.create()
    world.add(player, Transform(100, 100))
    world.add(player, Kinematics())
    world.add(player, Collider(32, 32))

    gravity = 1500.0
    speed = 400.0
    jump_speed = -600.0

    last_time = time.time()
    while app.running:
        now = time.time()
        dt = now - last_time
        last_time = now

        app.poll()
        input_mgr.poll()
        app.begin_frame()

        # Simple input handling
        keys = pygame.key.get_pressed()
        for e, tr, kin, col in world.query(Transform, Kinematics, Collider):
            target = 0.0
            if input_mgr.is_down('left'):
                target -= 1.0
            if input_mgr.is_down('right'):
                target += 1.0
            # horizontal smoothing
            accel = 12.0
            desired_vx = target * speed
            kin.vx += (desired_vx - kin.vx) * min(1.0, accel * dt)

            # gravity
            kin.vy += gravity * dt

            # Edge-trigger jump
            if input_mgr.was_pressed('jump') and kin.on_ground:
                kin.vy = jump_speed
                kin.on_ground = False

        # Update world (runs MovementSystem integration)
        world.update(dt)

        # Ground clamp AFTER physics update to avoid one-frame overlap
        for e, tr, kin, col in world.query(Transform, Kinematics, Collider):
            ground_y = app.screen.get_height() - 50
            if tr.y + col.h >= ground_y:
                tr.y = ground_y - col.h
                kin.vy = 0.0
                kin.on_ground = True
            else:
                kin.on_ground = False

        # Draw ground and player
        ground_rect = pygame.Rect(0, app.screen.get_height() - 50, app.screen.get_width(), 50)
        pygame.draw.rect(app.screen, (60, 60, 90), ground_rect)

        for e, tr, kin, col in world.query(Transform, Kinematics, Collider):
            rect = pygame.Rect(int(tr.x), int(tr.y), col.w, col.h)
            pygame.draw.rect(app.screen, (200, 230, 255), rect)

        app.end_frame()

    app.quit()


if __name__ == '__main__':
    main()


