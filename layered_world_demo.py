import pygame
import struct
import os
import random

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40
ROOM_TILES_X = WIDTH // TILE_SIZE
ROOM_TILES_Y = HEIGHT // TILE_SIZE
CHUNK_FOLDER = 'world_chunks'
ASSET_FOLDER = 'sample_tiles'

# --- Generate demo PNG assets ---
def generate_demo_tiles():
    if not os.path.isdir(ASSET_FOLDER):
        os.makedirs(ASSET_FOLDER)
    # Grass
    grass_path = os.path.join(ASSET_FOLDER, 'grass.png')
    if not os.path.exists(grass_path):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        surf.fill((60, 170, 65))
        pygame.draw.rect(surf, (22, 110, 25), (0, 20, 32, 12))  # darker grass base
        pygame.image.save(surf, grass_path)
    # Rock
    rock_path = os.path.join(ASSET_FOLDER, 'rock.png')
    if not os.path.exists(rock_path):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        surf.fill((0,0,0,0))
        pygame.draw.ellipse(surf, (130,130,140), (3,10,26,17))
        pygame.draw.ellipse(surf, (60,60,70), (7,16,18,12))
        pygame.image.save(surf, rock_path)
    # Platform
    plat_path = os.path.join(ASSET_FOLDER, 'platform.png')
    if not os.path.exists(plat_path):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        surf.fill((210, 180, 80,255))
        pygame.draw.rect(surf, (170,118,30), (0, 18, 32, 8))  # Brown base
        pygame.image.save(surf, plat_path)

tile_assets = {
    0: {'filename': None,           'name': 'empty',   'solid': False},
    1: {'filename': 'grass.png',    'name': 'grass',   'solid': True},
    2: {'filename': 'rock.png',     'name': 'rock',    'solid': True},
    3: {'filename': 'platform.png', 'name': 'platform','solid': True}
}

def load_tile_surface(tile_id):
    f = tile_assets[tile_id]['filename']
    if not f:
        return None
    path = os.path.join(ASSET_FOLDER, f)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, (TILE_SIZE, TILE_SIZE))

tile_surfaces = {}

# --- BINARY LOADERS AND SAVERS ---
def load_tile_layer(filename, width=ROOM_TILES_X, height=ROOM_TILES_Y):
    layer = []
    fullpath = os.path.join(CHUNK_FOLDER, filename)
    if not os.path.exists(fullpath):
        return [[0]*width for _ in range(height)]
    with open(fullpath, 'rb') as f:
        data = f.read()
        for y in range(height):
            row = [data[y*width + x] for x in range(width)]
            layer.append(row)
    return layer

def save_tile_layer(filename, tilemap):
    fullpath = os.path.join(CHUNK_FOLDER, filename)
    with open(fullpath, 'wb') as f:
        for row in tilemap:
            for tile_id in row:
                f.write(struct.pack('B', tile_id))

# Parallax bin: (x, y, w, h, speed, r, g, b) all floats except color as uint8
PARALLAX_STRUCT = struct.Struct('fffffBBB')
def load_parallax_layer(filename):
    shapes = []
    fullpath = os.path.join(CHUNK_FOLDER, filename)
    if not os.path.exists(fullpath):
        return shapes
    with open(fullpath, 'rb') as f:
        data = f.read()
        size = PARALLAX_STRUCT.size
        for i in range(0, len(data), size):
            fields = PARALLAX_STRUCT.unpack(data[i:i+size])
            x, y, w, h, speed, r, g, b = fields
            shapes.append({
                'rect': pygame.Rect(x, y, w, h),
                'vx': -abs(speed),  # Always move right-to-left
                'color': (int(r), int(g), int(b))
            })
    return shapes

def save_parallax_layer(filename, shapes):
    fullpath = os.path.join(CHUNK_FOLDER, filename)
    with open(fullpath, 'wb') as f:
        for shp in shapes:
            rect = shp['rect']
            vx = abs(shp['vx'])
            color = shp['color']
            f.write(PARALLAX_STRUCT.pack(rect.x, rect.y, rect.w, rect.h, vx, *color))

# Particle bin: (time, x, y, radius, r, g, b)
PARTICLE_STRUCT = struct.Struct('ffffBBB')
def load_particle_layer(filename):
    events = []
    fullpath = os.path.join(CHUNK_FOLDER, filename)
    if not os.path.exists(fullpath):
        return events
    with open(fullpath, 'rb') as f:
        data = f.read()
        size = PARTICLE_STRUCT.size
        for i in range(0, len(data), size):
            time, x, y, radius, r, g, b = PARTICLE_STRUCT.unpack(data[i:i+size])
            events.append({
                'time': time,
                'x': x,
                'y': y,
                'radius': radius,
                'color': (int(r),int(g),int(b))
            })
    return events

def save_particle_layer(filename, events):
    fullpath = os.path.join(CHUNK_FOLDER, filename)
    with open(fullpath, 'wb') as f:
        for e in events:
            f.write(PARTICLE_STRUCT.pack(e['time'], e['x'], e['y'], e['radius'], *e['color']))

# --- LAYER BASE ---
class Layer:
    def update(self, dt, events): pass
    def render(self, surf): pass

# --- BACKGROUND ---
class BackgroundLayer(Layer):
    def __init__(self, color): self.color=color
    def render(self, surf): surf.fill(self.color)

# --- PARALLAX (BIN-DRIVEN) ---
class ParallaxLayer(Layer):
    def __init__(self, parallax_shapes):
        self.shapes = parallax_shapes  # List of {'rect', 'vx', 'color'}
    def update(self, dt, events):
        for shp in self.shapes:
            shp['rect'].x += int(shp['vx'] * dt)
            # Wrap
            if shp['rect'].right < 0: shp['rect'].left = WIDTH
            if shp['rect'].left > WIDTH: shp['rect'].right = 0
    def render(self, surf):
        for shp in self.shapes:
            pygame.draw.ellipse(surf, shp['color'], shp['rect'], 0)

# --- TILE RENDER ---
def draw_tile(surf, tile_id, x, y):
    if tile_id in tile_assets and tile_assets[tile_id]['filename']:
        if tile_id not in tile_surfaces:
            tile_surfaces[tile_id] = load_tile_surface(tile_id)
        img = tile_surfaces[tile_id]
        surf.blit(img, (x,y))

# --- ACTUAL (TILES) ---
class ActualLayer(Layer):
    def __init__(self, tilemap): self.tilemap = tilemap
    def render(self, surf):
        for y, row in enumerate(self.tilemap):
            for x, tile_id in enumerate(row):
                draw_tile(surf, tile_id, x*TILE_SIZE, y*TILE_SIZE)

# --- COLLISION (TILES) ---
class CollisionLayer(Layer):
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.masks = {} # tile_id → Mask
    def render(self, surf):
        for y,row in enumerate(self.tilemap):
            for x,tile_id in enumerate(row):
                if tile_id in tile_assets and tile_assets[tile_id]['solid']:
                    # Draw red outline using mask (for prototype: just outline the nontransparent area)
                    if tile_id not in tile_surfaces:
                        tile_surfaces[tile_id] = load_tile_surface(tile_id)
                    surf_img = tile_surfaces[tile_id]
                    if tile_id not in self.masks:
                        self.masks[tile_id] = pygame.mask.from_surface(surf_img)
                    mask = self.masks[tile_id]
                    offset = (x*TILE_SIZE, y*TILE_SIZE)
                    # Draw red mask pixels
                    outline_color = (220,40,50)
                    points = mask.outline()
                    if points:
                        shifted_pts = [(px+offset[0], py+offset[1]) for (px,py) in points]
                        if len(shifted_pts) > 1:
                            pygame.draw.lines(surf, outline_color, True, shifted_pts, 2)

# --- DATA-DRIVEN PARTICLE LAYER ---
class TimedParticle:
    def __init__(self, t, x, y, radius, color):
        self.spawn_time = t
        self.init_x, self.init_y = x, y
        self.radius = radius
        self.color = color
        self.life = 0.8
        self.spawned = False
    def update(self, dt):
        self.life -= dt
        self.radius *= 0.98
    def draw(self, surf):
        if self.life>0:
            alpha = int(155 * max(0, self.life/0.8))
            surf_ = pygame.Surface((int(self.radius)*2, int(self.radius)*2), pygame.SRCALPHA)
            pygame.draw.circle(surf_, self.color+(alpha,), (int(self.radius),int(self.radius)), max(2,int(self.radius)))
            surf.blit(surf_, (int(self.init_x-self.radius),int(self.init_y-self.radius)), special_flags=pygame.BLEND_PREMULTIPLIED)

class Particle:
    def __init__(self, x, y, color=None, r=None):
        self.x = x + random.randint(-6, 6)
        self.y = y + random.randint(-6, 6)
        self.radius = r if r else random.randint(10, 16)
        self.color = color if color is not None else (240,230,70)
        self.life = 0.7 + random.random()*0.3
    def update(self, dt):
        self.life -= dt
        self.radius *= 0.98
    def draw(self, surf):
        if self.life > 0:
            alpha = int(200 * max(0, self.life/1.0))
            surf_ = pygame.Surface((int(self.radius)*2, int(self.radius)*2), pygame.SRCALPHA)
            pygame.draw.circle(surf_, self.color+(alpha,), (int(self.radius),int(self.radius)), max(2,int(self.radius)))
            surf.blit(surf_, (int(self.x-self.radius), int(self.y-self.radius)), special_flags=pygame.BLEND_PREMULTIPLIED)

class ParticleLayer(Layer):
    def __init__(self, event_list):
        self.timed_events = sorted([TimedParticle(e['time'],e['x'],e['y'],e['radius'],e['color']) for e in event_list], key=lambda e: e.spawn_time)
        self.time = 0
        self.spawned_particles = []
        self.mouse_particles = []
    def update(self, dt, events):
        self.time += dt
        # Trigger file-based events
        for tpe in self.timed_events:
            if not tpe.spawned and self.time >= tpe.spawn_time:
                self.spawned_particles.append(tpe)
                tpe.spawned = True
        self.spawned_particles = [p for p in self.spawned_particles if p.life>0.0]
        for p in self.spawned_particles: p.update(dt)
        # Mouse click particles
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for _ in range(random.randint(3,6)):
                    self.mouse_particles.append(Particle(mx,my))
        self.mouse_particles = [p for p in self.mouse_particles if p.life > 0.0]
        for p in self.mouse_particles: p.update(dt)
    def render(self, surf):
        for p in self.spawned_particles: p.draw(surf)
        for mp in self.mouse_particles: mp.draw(surf)

# --- FOREGROUND ---
class ForegroundLayer(Layer):
    def __init__(self, ground_y): self.y = ground_y
    def render(self, surf):
        fg_rect = pygame.Rect(0, self.y, WIDTH, 22)
        pygame.draw.rect(surf, (100,80,200), fg_rect)
        pygame.draw.arc(surf, (180,140,250), fg_rect.move(100,2).inflate(-200,10), 0.5, 2.5, 4)

# --- LAYERED WORLD ---
class LayeredWorld:
    def __init__(self, width, height):
        # --- Generate bin files for demo if missing ---
        # Actual/Collision ground/platforms as before
        actual_path = os.path.join(CHUNK_FOLDER, 'actual_layer.bin')
        collision_path = os.path.join(CHUNK_FOLDER, 'collision_layer.bin')
        if not os.path.exists(actual_path):
            tilemap = [[0]*ROOM_TILES_X for _ in range(ROOM_TILES_Y)]
            for y in range(ROOM_TILES_Y-2, ROOM_TILES_Y):
                for x in range(ROOM_TILES_X): tilemap[y][x] = 1
            for dx in range(3, 7): tilemap[8][dx] = 1
            for dx in range(10, 14): tilemap[6][dx] = 1
            save_tile_layer('actual_layer.bin', tilemap)
        if not os.path.exists(collision_path):
            save_tile_layer('collision_layer.bin', load_tile_layer('actual_layer.bin'))
        # Parallax: a few drifting shapes
        parallax_path = os.path.join(CHUNK_FOLDER, 'parallax_layer.bin')
        if not os.path.exists(parallax_path):
            default_shapes = []
            for template in [((145,170,195), 100, 6, (90,130)), ((95,110,180), 45, 7, (45,80))]:
                color, speed, n, size_rng = template
                for _ in range(n):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    w, h = [random.randint(*size_rng) for _ in range(2)]
                    default_shapes.append({'rect':pygame.Rect(x,y,w,h),'vx':-abs(speed),'color':color})
            save_parallax_layer('parallax_layer.bin', default_shapes)
        # Particle: some particles triggered at intervals
        particle_path = os.path.join(CHUNK_FOLDER, 'particle_layer.bin')
        if not os.path.exists(particle_path):
            evts = []
            for t in range(2, 16, 2):
                x = random.randint(WIDTH//5, WIDTH-WIDTH//5)
                y = random.randint(HEIGHT//3, HEIGHT-80)
                r = random.randint(13,23)
                color = (245,224,80)
                evts.append({'time': float(1.0*t), 'x': x, 'y': y, 'radius': r, 'color': color})
            save_particle_layer('particle_layer.bin', evts)
        # Load layers
        actual_tilemap = load_tile_layer('actual_layer.bin')
        collision_tilemap = load_tile_layer('collision_layer.bin')
        parallax_shapes = load_parallax_layer('parallax_layer.bin')
        particle_events = load_particle_layer('particle_layer.bin')
        ground_y = (ROOM_TILES_Y-2) * TILE_SIZE
        self.layers = [
            BackgroundLayer((110, 110, 110)),
            ParallaxLayer(parallax_shapes),
            ActualLayer(actual_tilemap),
            CollisionLayer(collision_tilemap),
            ParticleLayer(particle_events),
            ForegroundLayer(ground_y+40)
        ]
    def update(self, dt, events):
        for layer in self.layers:
            layer.update(dt, events)
    def render(self, surf):
        for layer in self.layers:
            layer.render(surf)

# --- MAIN LOOP ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Layered World Fully Data-driven Demo')
    clock = pygame.time.Clock()
    world = LayeredWorld(WIDTH, HEIGHT)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        world.update(dt, events)
        world.render(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    pygame.init()
    generate_demo_tiles()
    main()
