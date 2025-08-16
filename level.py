import pygame
import math
from settings import *
from player import Player, Projectile
from levels.tutorial_level import TUTORIAL_LEVEL, SpriteEnemy

class Tile(pygame.sprite.Sprite):
    """Basic tile for platforms and obstacles"""
    def __init__(self, pos, size, tile_type='platform'):
        super().__init__()
        self.tile_type = tile_type
        self.image = pygame.Surface((size, size))
        
        # Color based on tile type
        if tile_type == 'platform':
            self.image.fill(COLORS['platform'])
        elif tile_type == 'fire':
            self.image.fill(COLORS['fire'])
        elif tile_type == 'lava':
            self.image.fill((255, 100, 0))  # Bright orange for lava
        elif tile_type == 'wind':
            self.image.fill((150, 200, 255))  # Light blue for wind areas
        elif tile_type == 'energy':
            self.image.fill(COLORS['energy_tile'])  # Cyan for energy tiles
            
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self):
        # Add any tile-specific animations or behaviors here
        pass

class CollectibleItem(pygame.sprite.Sprite):
    """Collectible items like fragments and ability orbs"""
    def __init__(self, pos, item_type, region=None):
        super().__init__()
        self.item_type = item_type
        self.region = region
        self.image = pygame.Surface((24, 24))
        
        if item_type == 'fragment':
            self.image.fill(COLORS['crystal_fragment'])
        elif item_type == 'ability_orb':
            self.image.fill(COLORS['ability_orb'])
        elif item_type == 'crystal':
            self.image.fill(COLORS['crystal_fragment'])
            
        self.rect = self.image.get_rect(center=pos)
        self.float_offset = 0
        self.float_speed = 0.1
        
    def update(self):
        # Floating animation
        self.float_offset += self.float_speed
        self.rect.y += int(math.sin(self.float_offset) * 2)

class SimpleEnemy(pygame.sprite.Sprite):
    """Simple patrolling enemy"""
    def __init__(self, pos, patrol_distance=100):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(COLORS['enemy'])
        self.rect = self.image.get_rect(topleft=pos)
        
        self.speed = 2
        self.direction = 1
        self.start_x = pos[0]
        self.patrol_distance = patrol_distance
        self.health = 75  # Takes 3 hits to kill (25 damage per hit)
        self.max_health = 75
        
    def update(self):
        # Simple patrol behavior
        self.rect.x += self.speed * self.direction
        
        # Turn around at patrol boundaries
        if self.rect.x <= self.start_x - self.patrol_distance:
            self.direction = 1
        elif self.rect.x >= self.start_x + self.patrol_distance:
            self.direction = -1

class TutorialBoss(pygame.sprite.Sprite):
    """Simple tutorial boss"""
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((64, 64))
        self.image.fill((150, 0, 150))  # Purple boss
        self.rect = self.image.get_rect(center=pos)
        
        self.health = 200
        self.max_health = 200
        self.speed = 1
        self.direction = 1
        self.attack_timer = 0
        self.attack_cooldown = 120  # 2 seconds at 60 FPS
        
    def update(self):
        # Simple movement
        self.rect.x += self.speed * self.direction
        
        # Simple AI - change direction randomly
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.direction *= -1
            self.attack_timer = 0

class Level:
    """Enhanced level class with elemental mechanics"""
    
    def __init__(self, surface, level_data=None):
        self.display_surface = surface
        self.level_data = level_data or TUTORIAL_LEVEL
        
        # Sprite groups
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.boss = pygame.sprite.GroupSingle()
        self.projectiles = pygame.sprite.Group()  # New projectile group
        
        # Level state
        self.current_region = 'fire'  # Start in fire region
        self.transition_point = None
        self.boss_activated = False
        self.level_complete = False
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Setup level
        self.setup_level()
        
        # Tutorial state
        self.tutorial_stage = 'fire_section'
        self.puzzles_completed = []
        
    def setup_level(self):
        """Setup the level from layout data with proper tile alignment"""
        self.temp_player_spawn_tile = None
        
        for row_index, row in enumerate(self.level_data):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if cell == 'X':
                    tile = Tile((x, y), TILE_SIZE, 'platform')
                    self.tiles.add(tile)
                elif cell == 'L':
                    tile = Tile((x, y), TILE_SIZE, 'lava')
                    self.tiles.add(tile)
                elif cell == 'W':
                    tile = Tile((x, y), TILE_SIZE, 'wind')
                    self.tiles.add(tile)
                elif cell == 'N':
                    tile = Tile((x, y), TILE_SIZE, 'energy')
                    self.tiles.add(tile)
                elif cell == 'P':
                    self.temp_player_spawn_tile = (x, y)
                elif cell == 'E':
                    enemy = SimpleEnemy((x, y))
                    self.enemies.add(enemy)
                elif cell == 'F':
                    fragment = CollectibleItem((x + TILE_SIZE//2, y + TILE_SIZE//2), 'fragment', self.current_region)
                    self.collectibles.add(fragment)
                elif cell == 'A':
                    ability_orb = CollectibleItem((x + TILE_SIZE//2, y + TILE_SIZE//2), 'ability_orb')
                    self.collectibles.add(ability_orb)
                elif cell == 'B':
                    boss = TutorialBoss((x + TILE_SIZE//2, y + TILE_SIZE//2))
                    self.boss.add(boss)
                elif cell == 'T':
                    self.transition_point = (x, y)

        # Create player at spawn point
        if self.temp_player_spawn_tile:
            px, py = self.temp_player_spawn_tile
            # Find platform directly below the spawn point
            platform_below = None
            for tile in self.tiles:
                if tile.tile_type == 'platform' and tile.rect.collidepoint(px + TILE_SIZE//2, py + TILE_SIZE):
                    platform_below = tile
                    break
            
            # Position player on platform
            if platform_below:
                p_x = platform_below.rect.centerx - 16  # 32 width / 2
                p_y = platform_below.rect.top - 48      # 48 height
            else:
                p_x, p_y = px, py
                
            player_sprite = Player((p_x, p_y), self.display_surface)
            player_sprite.set_region(self.current_region)
            self.player.add(player_sprite)

    def handle_collisions(self):
        """Handle all collisions with proper tile alignment and improved movement"""
        player = self.player.sprite
        if not player:
            return

        # Reset collision states
        player.on_ground = False
        player.on_ceiling = False
        player.on_left = False
        player.on_right = False
        player.on_energy_tile = False
        player.at_edge = False  # Reset edge detection

        # Store original position for collision resolution
        original_x = player.rect.x
        original_y = player.rect.y

        # 1. Handle horizontal movement and collision
        # Apply horizontal movement from player's direction
        player.rect.x += int(player.direction.x)
        
        # Check horizontal collisions with platforms
        for tile in self.tiles:
            if tile.tile_type == 'platform' and player.rect.colliderect(tile.rect):
                if player.direction.x > 0:  # Moving right
                    player.rect.right = tile.rect.left
                    player.on_right = True
                    player.direction.x = 0  # Stop horizontal movement
                elif player.direction.x < 0:  # Moving left
                    player.rect.left = tile.rect.right
                    player.on_left = True
                    player.direction.x = 0  # Stop horizontal movement

        # 2. Handle vertical movement and collision
        # Apply gravity
        player.direction.y += player.gravity
        if player.direction.y > player.max_fall_speed:
            player.direction.y = player.max_fall_speed
            
        player.rect.y += int(player.direction.y)
        
        # Check vertical collisions with platforms
        for tile in self.tiles:
            if tile.tile_type == 'platform' and player.rect.colliderect(tile.rect):
                if player.direction.y > 0:  # Falling
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:  # Jumping
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        # Edge detection: Check if player is at the edge of a platform
        if player.on_ground:
            # We need to check if there's a platform directly in front of the player's feet
            # Check both left and right edges based on player's facing direction
            edge_check_distance = 8  # Smaller distance for more precise detection
            
            # Create a small rectangle in front of the player's feet
            if player.facing_right:
                edge_rect = pygame.Rect(
                    player.rect.right,  # Start from right edge of player
                    player.rect.bottom - 2,  # At player's feet level
                    edge_check_distance,
                    4  # Small height check
                )
            else:
                edge_rect = pygame.Rect(
                    player.rect.left - edge_check_distance,  # Start from left edge of player
                    player.rect.bottom - 2,  # At player's feet level
                    edge_check_distance,
                    4  # Small height check
                )
            
            # Check if there's a platform at the edge
            platform_at_edge = False
            for tile in self.tiles:
                if tile.tile_type == 'platform' and edge_rect.colliderect(tile.rect):
                    platform_at_edge = True
                    break
            
            # If player is on ground but there's no platform at the edge, they're at an edge
            if not platform_at_edge:
                player.at_edge = True
                print(f"Edge detected! Player at edge: {player.at_edge}, Facing: {'right' if player.facing_right else 'left'}")
            else:
                player.at_edge = False

        # 3. Handle special tile effects
        for tile in self.tiles:
            if player.rect.colliderect(tile.rect):
                if tile.tile_type == 'lava':
                    player.health -= 0.1
                elif tile.tile_type == 'energy':
                    player.on_energy_tile = True

        # 4. Handle enemy collisions
        for enemy in self.enemies:
            if player.rect.colliderect(enemy.rect):
                player.health -= 0.1  # Light damage
                
            # Check melee attack hits
            if player.melee_attacking and player.melee_attack_rect and player.melee_attack_rect.colliderect(enemy.rect):
                enemy.health -= player.melee_damage
                print(f"Enemy hit by melee! Health: {enemy.health}")
                if enemy.health <= 0:
                    enemy.kill()
                    print("Enemy defeated!")

        # 5. Handle collectible collisions
        for collectible in self.collectibles:
            if player.rect.colliderect(collectible.rect):
                self.collect_item(collectible)

        # 6. Handle boss collisions
        if self.boss.sprite and player.rect.colliderect(self.boss.sprite.rect):
            player.health -= 0.2
            if player.dash_timer > 0:
                self.boss.sprite.health -= 2
                print(f"Boss damaged by dash! Health: {self.boss.sprite.health}")

        # 7. Handle boss melee attacks
        if self.boss.sprite and player.melee_attacking and player.melee_attack_rect:
            if player.melee_attack_rect.colliderect(self.boss.sprite.rect):
                self.boss.sprite.health -= player.melee_damage
                print(f"Boss damaged by melee attack! Health: {self.boss.sprite.health}")

        # 8. Handle projectiles
        self.handle_projectiles()

        # Reset attack states
        player.melee_attacking = False
        player.ranged_attacking = False

    def handle_projectiles(self):
        """Handle projectile collisions and movement"""
        # Add new projectiles from player
        if self.player.sprite and self.player.sprite.ranged_attacking and self.player.sprite.current_projectile:
            self.projectiles.add(self.player.sprite.current_projectile)
            self.player.sprite.current_projectile = None
            
        # Update projectiles
        for projectile in self.projectiles:
            projectile.update()
            
            # Check projectile collisions with enemies
            for enemy in self.enemies:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.health -= projectile.damage
                    projectile.kill()
                    if enemy.health <= 0:
                        enemy.kill()
                    break
                    
            # Check projectile collisions with boss
            if self.boss.sprite and projectile.rect.colliderect(self.boss.sprite.rect):
                self.boss.sprite.health -= projectile.damage
                projectile.kill()
                break

    def collect_item(self, item):
        """Handle item collection"""
        if item.item_type == 'fragment':
            self.player.sprite.collect_fragment(item.region)
            print(f"Collected {item.region} fragment!")
        elif item.item_type == 'ability_orb':
            # Unlock random ability for current region
            if self.current_region == 'fire':
                abilities = ['fire_dash', 'fire_projectile', 'fire_aura']
            elif self.current_region == 'air':
                abilities = ['air_jump', 'air_dash', 'air_glide']
            else:
                abilities = ['fire_dash']  # Default
                
            import random
            ability = random.choice(abilities)
            self.player.sprite.unlock_ability(ability)
            print(f"Unlocked {ability}!")
            
        item.kill()

    def check_transitions(self):
        """Check if player has reached transition point"""
        if self.transition_point and self.player.sprite:
            player = self.player.sprite
            transition_rect = pygame.Rect(self.transition_point[0], self.transition_point[1], TILE_SIZE, TILE_SIZE)
            
            if player.rect.colliderect(transition_rect) and self.tutorial_stage == 'fire_section':
                self.transition_to_wind()
                
    def transition_to_wind(self):
        """Transition from fire to wind region"""
        self.current_region = 'air'
        self.tutorial_stage = 'wind_section'
        self.player.sprite.set_region('air')
        print("🌪️ REGION TRANSITION! Entering wind region! You can now unlock air abilities.")
        
    def check_tutorial_progress(self):
        """Check tutorial progression and give hints"""
        player = self.player.sprite
        
        if self.tutorial_stage == 'fire_section':
            if len(player.unlocked_abilities) == 0:
                # Hint about collecting ability orb
                pass
        elif self.tutorial_stage == 'wind_section':
            if not self.boss_activated and len(self.collectibles.sprites()) == 0:
                self.boss_activated = True
                print("Boss fight begins!")
                
    def update_camera(self):
        """Update camera to follow player"""
        if self.player.sprite:
            player = self.player.sprite
            
            # Calculate target camera position (center player on screen)
            target_x = SCREEN_WIDTH // 2 - player.rect.centerx
            target_y = SCREEN_HEIGHT // 2 - player.rect.centery
            
            # Apply camera bounds
            level_width = len(self.level_data[0]) * TILE_SIZE
            level_height = len(self.level_data) * TILE_SIZE
            
            # Clamp camera to level bounds
            self.camera_x = max(SCREEN_WIDTH - level_width, min(0, target_x))
            self.camera_y = max(SCREEN_HEIGHT - level_height, min(0, target_y))
            
    def draw_ui(self):
        """Draw UI elements"""
        player = self.player.sprite
        if not player:
            return
            
        # Health bar
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.health / player.max_health
        
        # Background
        health_bg = pygame.Rect(10, 10, health_bar_width, health_bar_height)
        pygame.draw.rect(self.display_surface, (100, 0, 0), health_bg)
        
        # Health fill
        health_fill = pygame.Rect(10, 10, health_bar_width * health_ratio, health_bar_height)
        pygame.draw.rect(self.display_surface, (0, 200, 0), health_fill)
        
        # Energy bar
        energy_bar_width = 200
        energy_bar_height = 15
        energy_ratio = player.energy / player.max_energy
        
        # Energy background
        energy_bg = pygame.Rect(10, 35, energy_bar_width, energy_bar_height)
        pygame.draw.rect(self.display_surface, COLORS['energy_bar_bg'], energy_bg)
        
        # Energy fill
        energy_fill = pygame.Rect(10, 35, energy_bar_width * energy_ratio, energy_bar_height)
        pygame.draw.rect(self.display_surface, COLORS['energy_bar'], energy_fill)
        
        # Energy label
        font = pygame.font.Font(None, 24)
        energy_text = font.render("ENERGY", True, (255, 255, 255))
        self.display_surface.blit(energy_text, (10, 55))
        
        # Boss health bar (if boss exists)
        if self.boss.sprite:
            boss_health_ratio = self.boss.sprite.health / self.boss.sprite.max_health
            boss_bg = pygame.Rect(SCREEN_WIDTH - 210, 10, health_bar_width, health_bar_height)
            pygame.draw.rect(self.display_surface, (100, 0, 0), boss_bg)
            boss_fill = pygame.Rect(SCREEN_WIDTH - 210, 10, health_bar_width * boss_health_ratio, health_bar_height)
            pygame.draw.rect(self.display_surface, (200, 0, 0), boss_fill)
            
            # Boss label
            font = pygame.font.Font(None, 24)
            boss_text = font.render("BOSS", True, (255, 255, 255))
            self.display_surface.blit(boss_text, (SCREEN_WIDTH - 210, 35))
        
        # Abilities display
        abilities = player.get_available_abilities()
        for i, ability in enumerate(abilities[:3]):
            ability_rect = pygame.Rect(10 + i * 60, 80, 50, 30)
            pygame.draw.rect(self.display_surface, (0, 0, 150), ability_rect)
            
            # Draw ability name (simplified)
            font = pygame.font.Font(None, 24)
            keys = "Q E R"
            text = font.render(keys[i*2], True, (255, 255, 255))
            self.display_surface.blit(text, (ability_rect.x + 20, ability_rect.y + 5))
            
        # Tutorial hints
        if self.tutorial_stage == 'fire_section':
            hint_text = "WASD to move, Space to jump (hold for higher), Q/E/R for abilities, Left Click for melee, Right Click for ranged!"
        elif self.tutorial_stage == 'wind_section':
            hint_text = "Air abilities unlocked! Stand on cyan tiles to recharge energy for ranged attacks!"
        else:
            hint_text = "Try wall jumping by pressing against walls and jumping!"
            
        if hint_text:
            font = pygame.font.Font(None, 36)
            text = font.render(hint_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            self.display_surface.blit(text, text_rect)
        
        # DEBUG: Show player position and collision states
        if player:
            debug_font = pygame.font.Font(None, 24)
            pos_text = f"Pos: ({player.rect.x}, {player.rect.y})"
            ground_text = f"On Ground: {player.on_ground}"
            edge_text = f"At Edge: {player.at_edge}"
            was_edge_text = f"Was At Edge: {player.was_at_edge}"
            coyote_text = f"Coyote: {player.coyote_timer}"
            jump_buffer_text = f"Jump Buffer: {player.jump_buffer_timer}"
            velocity_text = f"Velocity: ({player.direction.x:.1f}, {player.direction.y:.1f})"
            speed_text = f"Speed: {abs(player.direction.x):.1f}"
            wall_slide_text = f"Wall Slide: {player.wall_sliding}"
            wall_jump_text = f"Wall Jump CD: {player.wall_jump_timer}"
            jumping_text = f"Jumping: {player.is_jumping}"
            
            self.display_surface.blit(debug_font.render(pos_text, True, (255, 255, 255)), (10, 150))
            self.display_surface.blit(debug_font.render(ground_text, True, (255, 255, 255)), (10, 170))
            self.display_surface.blit(debug_font.render(edge_text, True, (255, 255, 255)), (10, 190))
            self.display_surface.blit(debug_font.render(was_edge_text, True, (255, 255, 255)), (10, 210))
            self.display_surface.blit(debug_font.render(coyote_text, True, (255, 255, 255)), (10, 230))
            self.display_surface.blit(debug_font.render(jump_buffer_text, True, (255, 255, 255)), (10, 250))
            self.display_surface.blit(debug_font.render(velocity_text, True, (255, 255, 255)), (10, 270))
            self.display_surface.blit(debug_font.render(speed_text, True, (255, 255, 255)), (10, 290))
            self.display_surface.blit(debug_font.render(wall_slide_text, True, (255, 255, 255)), (10, 310))
            self.display_surface.blit(debug_font.render(wall_jump_text, True, (255, 255, 255)), (10, 330))
            self.display_surface.blit(debug_font.render(jumping_text, True, (255, 255, 255)), (10, 350))
            
    def draw(self):
        """Draw everything with proper camera offset"""
        # Clear screen
        self.display_surface.fill(COLORS['background'])
        
        # Create a surface for the world
        world_surface = pygame.Surface((len(self.level_data[0]) * TILE_SIZE, len(self.level_data) * TILE_SIZE))
        world_surface.fill(COLORS['background'])
        
        # Draw all sprites to world surface
        self.tiles.draw(world_surface)
        self.collectibles.draw(world_surface)
        self.enemies.draw(world_surface)
        self.projectiles.draw(world_surface)
        self.boss.draw(world_surface)
        self.player.draw(world_surface)
        
        # Draw melee attack visual
        player = self.player.sprite
        if player and player.melee_visual_timer > 0 and player.melee_attack_rect:
            pygame.draw.rect(world_surface, (255, 0, 0), player.melee_attack_rect, 2)
        
        # DEBUG: Draw collision boxes (uncomment to see collision areas)
        # Draw player collision box
        if player:
            pygame.draw.rect(world_surface, (0, 255, 0), player.rect, 1)
            
            # Draw edge detection area
            if player.on_ground:
                edge_check_distance = 8
                if player.facing_right:
                    edge_rect = pygame.Rect(
                        player.rect.right,
                        player.rect.bottom - 2,
                        edge_check_distance,
                        4
                    )
                else:
                    edge_rect = pygame.Rect(
                        player.rect.left - edge_check_distance,
                        player.rect.bottom - 2,
                        edge_check_distance,
                        4
                    )
                edge_color = (255, 0, 255) if player.at_edge else (0, 255, 255)  # Magenta if at edge, cyan if not
                pygame.draw.rect(world_surface, edge_color, edge_rect, 2)
        
        # Draw platform collision boxes
        for tile in self.tiles:
            if tile.tile_type == 'platform':
                pygame.draw.rect(world_surface, (255, 255, 0), tile.rect, 1)
        
        # Draw world surface to screen with camera offset
        self.display_surface.blit(world_surface, (self.camera_x, self.camera_y))
        
        # Draw UI (not affected by camera)
        self.draw_ui()
        
    def update(self):
        """Update level logic"""
        if self.player.sprite:
            self.player.sprite.update()
            
        self.enemies.update()
        self.boss.update()
        self.collectibles.update()
        
        self.handle_collisions()
        
        # Update coyote time AFTER collision detection so it can detect ground transitions
        if self.player.sprite:
            self.player.sprite.update_coyote_time()
            
        self.check_transitions()
        self.check_tutorial_progress()
        self.update_camera()
