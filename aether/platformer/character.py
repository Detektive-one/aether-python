from ..ecs.world import World
from ..ecs.entity import EntityId
from ..physics.physics import Transform, Kinematics, Collider
from .components import Controller, Params, JumpState, PlayerTag


class Character:
    def __init__(self, world: World, x: float, y: float, w: int = 32, h: int = 48,
                 params: Params | None = None):
        self.world = world
        self.entity: EntityId = world.create()
        world.add(self.entity, Transform(x, y))
        world.add(self.entity, Kinematics())
        world.add(self.entity, Collider(w, h))
        world.add(self.entity, Controller())
        world.add(self.entity, JumpState())
        world.add(self.entity, params or Params())
        world.add(self.entity, PlayerTag())

    def add(self, component):
        self.world.add(self.entity, component)
        return self

    def get(self, comp_cls):
        return self.world.get(self.entity, comp_cls)


