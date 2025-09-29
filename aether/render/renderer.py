import pygame
from ..ecs.system import System


class RenderSystem(System):
    priority = 100

    def __init__(self, world, assets=None, surface=None, camera=None):
        super().__init__(world)
        self.assets = assets
        self.surface = surface
        self.camera = camera

    def update(self, dt: float):
        if not self.surface:
            return
        # Placeholder: systems that draw should do so here.
        # Actual sprite drawing will be added when we wire components.
        pass


