class System:
    """Base class for systems. Override update(dt)."""
    priority = 0
    def __init__(self, world):
        self.world = world
    def update(self, dt: float):
        pass


