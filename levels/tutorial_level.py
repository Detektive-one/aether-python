import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import COLORS

# Tutorial Level Layout
# Format: X = platform, L = lava, P = player start, E = enemy, F = fragment,
# A = ability orb, C = crystal, W = wind, B = boss, T = transition point, N = energy tile

TUTORIAL_LEVEL = [
    '                                                              ',
    '                                                              ',
    '               F                                              ',
    '            XXXXX                                             ',
    '  P      L                    E            A                 ',
    'XXXXX         XXX       XXXXX     XXXXX         XXXXX   T   ',
    '    X         X           X          X             X         ',
    '    X    E    X     F     X     E    X       A     X    XXX  ',
    '    XXX       XXX         XXX        XXX           XXX  X    ',
    'L                     A                   W              X    ',
    'XXXXXXXXX    XXXXXXXXXXXXXXXXXXXX    XXXXXXX                X    ',
    '                                   X                      X    ',
    '                                  X                      X    ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      B   X    ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

# New tutorial level with better coyote jump testing
TUTORIAL_LEVEL_IMPROVED = [
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '  P                                                                             ',
    'XXXXX                                                                           ',
    '                                                                                ',
    '        F                                                                       ',
    '      XXXXX                                                                     ',
    '                                                                                ',
    '              E                                                                ',
    '            XXXXX                                                               ',
    '                                                                                ',
    '                      A                                                        ',
    '                    XXXXX                                                       ',
    '                                                                                ',
    '                            F                                                  ',
    '                          XXXXX                                                 ',
    '                                                                                ',
    '                                    E                                          ',
    '                                  XXXXX                                         ',
    '                                                                                ',
    '                                          A                                    ',
    '                                        XXXXX                                   ',
    '                                                                                ',
    '                                                T                              ',
    '                                              XXXXX                             ',
    '                                                                                ',
    '                                                      B                        ',
    '                                                    XXXXX                       ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

# New test level for Hollow Knight style movement
TUTORIAL_LEVEL_MOVEMENT_TEST = [
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '  P                                                                             ',
    'XXXXX                                                                           ',
    '                                                                                ',
    '        F                                                                       ',
    '      XXXXX                                                                     ',
    '                                                                                ',
    '              E                                                                ',
    '            XXXXX                                                               ',
    '                                                                                ',
    '                      A                                                        ',
    '                    XXXXX                                                       ',
    '                                                                                ',
    '                            F                                                  ',
    '                          XXXXX                                                 ',
    '                                                                                ',
    '                                    E                                          ',
    '                                  XXXXX                                         ',
    '                                                                                ',
    '                                          A                                    ',
    '                                        XXXXX                                   ',
    '                                                                                ',
    '                                                T                              ',
    '                                              XXXXX                             ',
    '                                                                                ',
    '                                                      B                        ',
    '                                                    XXXXX                       ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

# Wall jumping test level with vertical walls
TUTORIAL_LEVEL_WALL_JUMP = [
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '  P                                                                             ',
    'XXXXX                                                                           ',
    '                                                                                ',
    '        F                                                                       ',
    '      XXXXX                                                                     ',
    '                                                                                ',
    '              E                                                                ',
    '            XXXXX                                                               ',
    '                                                                                ',
    '                      A                                                        ',
    '                    XXXXX                                                       ',
    '                                                                                ',
    '                            F                                                  ',
    '                          XXXXX                                                 ',
    '                                                                                ',
    '                                    E                                          ',
    '                                  XXXXX                                         ',
    '                                                                                ',
    '                                          A                                    ',
    '                                        XXXXX                                   ',
    '                                                                                ',
    '                                                T                              ',
    '                                              XXXXX                             ',
    '                                                                                ',
    '                                                      B                        ',
    '                                                    XXXXX                       ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

# Simple wall jump test
TUTORIAL_LEVEL_SIMPLE_WALL_JUMP = [
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '  P                                                                             ',
    'XXXXX                                                                           ',
    '                                                                                ',
    '        F                                                                       ',
    '      XXXXX                                                                     ',
    '                                                                                ',
    '              E                                                                ',
    '            XXXXX                                                               ',
    '                                                                                ',
    '                      A                                                        ',
    '                    XXXXX                                                       ',
    '                                                                                ',
    '                            F                                                  ',
    '                          XXXXX                                                 ',
    '                                                                                ',
    '                                    E                                          ',
    '                                  XXXXX                                         ',
    '                                                                                ',
    '                                          A                                    ',
    '                                        XXXXX                                   ',
    '                                                                                ',
    '                                                T                              ',
    '                                              XXXXX                             ',
    '                                                                                ',
    '                                                      B                        ',
    '                                                    XXXXX                       ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

# Tutorial level with energy tiles for testing ranged attacks
TUTORIAL_LEVEL_WITH_ENERGY = [
    '                                                              ',
    '                                                              ',
    '               F                                              ',
    '            XXXXX                                             ',
    '  P      L                    E            A                 ',
    'XXXXX         XXX       XXXXX     XXXXX         XXXXX   T   ',
    '    X         X           X          X             X         ',
    '    X    E    X     F     X     E    X       A     X    XXX  ',
    '    XXX       XXX         XXX        XXX           XXX  X    ',
    'L                     A                   W              X    ',
    'XXXXXXXXX    XXXXXXXXXXXXXXXXXXXX    XXXXXXX                X    ',
    '                                   X                      X    ',
    '                                  X                      X    ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      B   X    ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

# Placeholder mechanics for tutorial puzzles
# These can be expanded upon based on game logic mechanics

def fire_puzzle_1(player):
    """Simple fire spinning obstacle"""
    # TODO: Implement spinning fire obstacle
    print("Player navigates the spinning fire obstacle")
    

def fire_puzzle_2(player):
    """Button press to lower fire gate"""
    # TODO: Implement button and gate mechanics
    print("Player presses button to lower gate")
    

def transition_to_wind_region(player):
    """Transition to wind region"""
    # TODO: Implement transition mechanics
    print("Transition to wind region")
    

def wind_puzzle_1(player):
    """Use air dash to cross large gap"""
    if player.can_use_ability('air_dash'):
        player.activate_ability('air_dash')
        print("Player uses air dash!")
    

def wind_puzzle_2(player):
    """Navigate moving platforms using air abilities"""
    # TODO: Implement moving platforms
    print("Player navigates moving platforms")
    

def boss_fight(player):
    """Simple boss fight mechanics"""
    # TODO: Implement basic boss fight
    print("Boss fight initiated!")

# Define small sprite enemies
class SpriteEnemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(COLORS['enemy'])
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 2
        self.direction = 1  # Right
        self.boundaries = (pos[0] - 50, pos[0] + 50)

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= self.boundaries[0] or self.rect.right >= self.boundaries[1]:
            self.direction *= -1  # Change direction on boundaries

# Simple edge detection test level
TUTORIAL_LEVEL_EDGE_TEST = [
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '  P                                                                             ',
    'XXXXX                                                                           ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    '                                                                                ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]
