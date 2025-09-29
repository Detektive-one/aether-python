import pygame


class App:
    """Minimal application shell. Integrate with your game loop."""

    def __init__(self, size=(1200, 800), caption='Aether App', fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def begin_frame(self):
        self.screen.fill((20, 20, 30))

    def end_frame(self):
        pygame.display.flip()
        self.clock.tick(self.fps)

    def quit(self):
        pygame.quit()


