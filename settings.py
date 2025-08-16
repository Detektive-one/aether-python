# Game Configuration
import pygame

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 64
FPS = 60

# Colors for placeholder tiles (will be replaced with sprites later)
COLORS = {
    'background': (20, 20, 30),
    'earth': (101, 67, 33),
    'fire': (220, 50, 30),
    'water': (30, 100, 220),
    'air': (200, 200, 240),
    'space': (50, 20, 80),
    'platform': (100, 100, 100),
    'player': (255, 255, 255),
    'enemy': (200, 50, 50),
    'crystal_fragment': (255, 215, 0),
    'ability_orb': (100, 255, 100),
    'portal': (255, 100, 255),
    'energy_tile': (0, 255, 255),  # Cyan for energy tiles
    'projectile': (255, 255, 0),   # Yellow for projectiles
    'energy_bar': (0, 150, 255),   # Blue for energy bar
    'energy_bar_bg': (50, 50, 100) # Dark blue for energy bar background
}

# Element types
ELEMENTS = ['earth', 'fire', 'water', 'air', 'space']

# Region adjacency (pentagon layout)
REGION_ADJACENCY = {
    'earth': ['fire', 'space'],
    'fire': ['earth', 'water'], 
    'water': ['fire', 'air'],
    'air': ['water', 'space'],
    'space': ['air', 'earth']
}

# Element interactions (what cancels what)
ELEMENT_WEAKNESSES = {
    'earth': 'air',
    'fire': 'water',
    'water': 'earth',
    'air': 'fire',
    'space': 'space'  # space cancels itself
}

# Game progression
LEVELS_PER_REGION = 5
HIDDEN_LEVELS_PER_REGION = 2
TOTAL_REGIONS = 5
FRAGMENTS_NEEDED = LEVELS_PER_REGION  # 5 fragments to form crystal

# Player stats
PLAYER_SPEED = 6
PLAYER_JUMP_STRENGTH = -16  # Increased from -12 for better tap jumps
GRAVITY = 0.8
MAX_FALL_SPEED = 16

# Coyote jump settings
COYOTE_TIME = 8  # frames (about 0.13 seconds at 60 FPS)

# Combat settings
MELEE_ATTACK_DAMAGE = 25
RANGED_ATTACK_DAMAGE = 12  # Half of melee damage
MELEE_ATTACK_RANGE = 60
RANGED_ATTACK_RANGE = TILE_SIZE * 3  # 3 tiles max distance
MELEE_ATTACK_COOLDOWN = 500  # milliseconds
RANGED_ATTACK_COOLDOWN = 300  # milliseconds
PROJECTILE_SPEED = 8
PROJECTILE_WOBBLE_AMOUNT = 2  # pixels
PROJECTILE_WOBBLE_SPEED = 0.3  # radians per frame

# Energy system
MAX_ENERGY = 100
RANGED_ATTACK_ENERGY_COST = 15
ENERGY_REGEN_RATE = 1  # energy per frame when on energy tile
ENERGY_REGEN_COOLDOWN = 0  # frames between regen ticks

# Level layouts - simple placeholder for now
# Format: X = platform, P = player start, E = enemy, F = fragment, A = ability orb, B = boss, H = hidden entrance
# L = lava, W = wind, T = transition, N = energy tile
EARTH_LEVEL_1 = [
    '                                                                       ',
    '                                       XXX                             ',
    '                                                                       ',
    '       XXX            XX      XXXXXX       F         A                ',
    ' XX P                                X                XX               ',
    ' XXXX         XX         XX           X                     XXX        ',
    ' XXXX       XX                    X             XXX                XX  ',
    ' XX    X  XXXX    XX  XX     X    E     X  X   XX       XX  XXX        ',
    '       X  XXXX    X   XXX    X  X  X     X  X  X   XXX            X    ',
    '    XXXXX XXXXXX  XX  XXXX    XXXXXXXXXXX  XXXXXXXXXXXX  XX    XXXX    ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

FIRE_LEVEL_1 = [
    '                                                                       ',
    '                                                                       ',
    '               F                               A                       ',
    '       XXX            XX      XXXXXX                     XX           ',
    ' XX P                                X                XX               ',
    ' XXXX         XX         XX           X                     XXX        ',
    ' XXXX       XX                    X      E      XXX                XX  ',
    ' XX    X  XXXX    XX  XX     X          X  X   XX       XX  XXX        ',
    '       X  XXXX    X   XXX    X  X  X     X  X  X   XXX            X    ',
    '    XXXXX XXXXXX  XX  XXXX    XXXXXXXXXXX  XXXXXXXXXXXX  XX    XXXX    ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

# Simple test levels for each element
LEVEL_TEMPLATES = {
    'earth': [EARTH_LEVEL_1],
    'fire': [FIRE_LEVEL_1],
    'water': [EARTH_LEVEL_1],  # Will customize later
    'air': [EARTH_LEVEL_1],    # Will customize later  
    'space': [EARTH_LEVEL_1]   # Will customize later
}

# Game states
class GameState:
    MENU = "menu"
    REGION_SELECT = "region_select" 
    PLAYING = "playing"
    INVENTORY = "inventory"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"

# Sound settings (placeholder for now)
MASTER_VOLUME = 0.7
SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.6

# Input mappings
CONTROLS = {
    'move_left': pygame.K_a,
    'move_right': pygame.K_d, 
    'move_up': pygame.K_w,
    'move_down': pygame.K_s,
    'jump': pygame.K_SPACE,
    'ability_1': pygame.K_q,
    'ability_2': pygame.K_e,
    'ability_3': pygame.K_r,
    'melee_attack': 'MOUSE_LEFT',
    'ranged_attack': 'MOUSE_RIGHT',
    'pause': pygame.K_ESCAPE,
    'inventory': pygame.K_TAB
}
