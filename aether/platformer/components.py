from ..ecs.component import Component


class Controller(Component):
    def __init__(self):
        self.left = False
        self.right = False
        self.jump_pressed = False  # edge


class Params(Component):
    def __init__(self, speed=360.0, accel=18.0, max_speed=260.0,
                 gravity=1500.0, jump_speed=-600.0,
                 friction_ground=12.0, friction_air=2.0,
                 coyote_time=0.12, jump_buffer=0.10):
        self.speed = speed
        self.accel = accel
        self.max_speed = max_speed
        self.gravity = gravity
        self.jump_speed = jump_speed
        self.friction_ground = friction_ground
        self.friction_air = friction_air
        self.coyote_time = coyote_time
        self.jump_buffer = jump_buffer


class JumpState(Component):
    def __init__(self):
        self.on_ground = False
        self.was_on_ground = False
        self.coyote = 0.0
        self.buffer = 0.0


class PlayerTag(Component):
    pass


