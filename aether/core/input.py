import pygame


class Input:
    def __init__(self, mapping=None):
        # Default PC mapping; can be extended to controllers later
        self.mapping = mapping or {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_SPACE,
            'quit': pygame.K_ESCAPE,
        }
        self._prev = pygame.key.get_pressed()
        self._curr = self._prev

    def poll(self):
        self._prev = self._curr
        self._curr = pygame.key.get_pressed()

    def is_down(self, action: str) -> bool:
        key = self.mapping.get(action)
        return bool(self._curr[key]) if key is not None else False

    def was_pressed(self, action: str) -> bool:
        key = self.mapping.get(action)
        return bool(self._curr[key] and not self._prev[key]) if key is not None else False


