class Camera:
    def __init__(self, width: int, height: int):
        self.x = 0.0
        self.y = 0.0
        self.width = width
        self.height = height

    def follow(self, tx: float, ty: float, slowness: float = 0.15):
        self.x += (tx - self.width / 2 - self.x) * slowness
        self.y += (ty - self.height / 2 - self.y) * slowness


