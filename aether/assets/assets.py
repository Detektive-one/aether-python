import pygame


class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, key: str, path: str):
        self.images[key] = pygame.image.load(path).convert_alpha()

    def get_image(self, key: str):
        return self.images.get(key)


