from ..ecs.component import Component
from ..ecs.system import System


class Transform(Component):
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)


class Kinematics(Component):
    def __init__(self):
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.on_ground = False


class Collider(Component):
    def __init__(self, w: int, h: int, solid: bool = True):
        self.w = int(w)
        self.h = int(h)
        self.solid = bool(solid)


class MovementSystem(System):
    priority = 20

    def update(self, dt: float):
        # Placeholder integration: vx/vy -> position
        for e, tr, kin in self.world.query(Transform, Kinematics):
            tr.x += kin.vx * dt
            tr.y += kin.vy * dt


