import pygame

from ..ecs.system import System
from ..physics.physics import Transform, Kinematics, Collider
from .components import Controller, Params, JumpState


class InputSystem(System):
    priority = 10
    def __init__(self, world, input_mgr):
        super().__init__(world)
        self.input = input_mgr

    def update(self, dt: float):
        for e, ctrl in self.world.query(Controller):
            left = self.input.is_down('left')
            right = self.input.is_down('right')
            ctrl.left = left
            ctrl.right = right
            ctrl.jump_pressed = self.input.was_pressed('jump')


class MovementSystem(System):
    priority = 20
    def update(self, dt: float):
        for e, tr, kin, ctrl, prm, js in self.world.query(Transform, Kinematics, Controller, Params, JumpState):
            target = (-1.0 if ctrl.left else 0.0) + (1.0 if ctrl.right else 0.0)
            desired_vx = target * prm.speed
            kin.vx += (desired_vx - kin.vx) * min(1.0, prm.accel * dt)

            damp = prm.friction_ground if js.on_ground else prm.friction_air
            kin.vx += (-kin.vx) * min(1.0, damp * dt)

            kin.vx = max(-prm.max_speed, min(prm.max_speed, kin.vx))
            kin.vy += prm.gravity * dt

            if ctrl.jump_pressed:
                js.buffer = prm.jump_buffer

            if js.buffer > 0.0 and (js.on_ground or js.coyote > 0.0):
                kin.vy = prm.jump_speed
                js.on_ground = False
                js.coyote = 0.0
                js.buffer = 0.0

            # Do not integrate position here; collision system will apply axis-wise movement

            # Timers
            if js.was_on_ground and not js.on_ground and js.coyote <= 0.0:
                js.coyote = prm.coyote_time
            if js.on_ground:
                js.coyote = 0.0
            else:
                js.coyote = max(0.0, js.coyote - dt)
            js.buffer = max(0.0, js.buffer - dt)
            js.was_on_ground = js.on_ground


class TileCollisionSystem(System):
    priority = 30
    def __init__(self, world, tiles):
        super().__init__(world)
        self.tiles = tiles  # list of pygame.Rect

    def update(self, dt: float):
        for e, tr, kin, col, js in self.world.query(Transform, Kinematics, Collider, JumpState):
            ent = pygame.Rect(int(tr.x), int(tr.y), col.w, col.h)
            # Vertical movement and resolve first
            ent.y += int(kin.vy * dt)
            collided_v = False
            for t in self.tiles:
                if ent.colliderect(t):
                    if kin.vy > 0:
                        ent.bottom = t.top
                        kin.vy = 0.0
                        js.on_ground = True
                        collided_v = True
                    elif kin.vy < 0:
                        ent.top = t.bottom
                        kin.vy = 0.0
                    break
            if not collided_v:
                js.on_ground = False

            # Horizontal movement and resolve
            ent.x += int(kin.vx * dt)
            for t in self.tiles:
                if ent.colliderect(t):
                    if kin.vx > 0:
                        ent.right = t.left
                    elif kin.vx < 0:
                        ent.left = t.right
                    kin.vx = 0.0
                    break

            tr.x, tr.y = ent.x, ent.y


