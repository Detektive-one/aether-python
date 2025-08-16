import pygame
import math
from settings import *

class Projectile(pygame.sprite.Sprite):
    """Ranged attack projectile"""
    def __init__(self, pos, direction, damage):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(COLORS['projectile'])
        pygame.draw.circle(self.image, COLORS['projectile'], (4, 4), 4)
        self.rect = self.image.get_rect(center=pos)
        
        self.direction = pygame.math.Vector2(direction).normalize()
        self.speed = PROJECTILE_SPEED
        self.damage = damage
        self.max_distance = RANGED_ATTACK_RANGE
        self.distance_traveled = 0
        self.start_pos = pygame.math.Vector2(pos)
        
        # Wobble effect
        self.wobble_time = 0
        self.wobble_amount = PROJECTILE_WOBBLE_AMOUNT
        self.wobble_speed = PROJECTILE_WOBBLE_SPEED
        
    def update(self):
        # Calculate base movement
        movement = self.direction * self.speed
        
        # Add wobble effect
        self.wobble_time += self.wobble_speed
        wobble_x = math.sin(self.wobble_time) * self.wobble_amount
        wobble_y = math.cos(self.wobble_time * 0.7) * self.wobble_amount
        
        # Apply movement with wobble
        self.rect.x += int(movement.x + wobble_x)
        self.rect.y += int(movement.y + wobble_y)
        
        # Track distance traveled
        current_pos = pygame.math.Vector2(self.rect.center)
        self.distance_traveled = current_pos.distance_to(self.start_pos)
        
        # Destroy if max distance reached
        if self.distance_traveled >= self.max_distance:
            self.kill()

class Player(pygame.sprite.Sprite):
    """Player character with elemental abilities"""
    
    def __init__(self, pos, surface):
        super().__init__()
        
        # Graphics
        self.image = pygame.Surface((32, 48))
        self.image.fill(COLORS['player'])
        self.rect = self.image.get_rect(topleft=pos)
        self.display_surface = surface
        
        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.jump_speed = PLAYER_JUMP_STRENGTH
        self.max_fall_speed = MAX_FALL_SPEED
        
        # Enhanced movement (Hollow Knight style)
        self.air_speed = PLAYER_SPEED * 0.8  # Slightly slower in air
        self.air_control = 0.7  # Reduced air control
        self.max_speed = 8  # Maximum horizontal speed
        self.acceleration = 0.5  # How quickly speed changes
        self.friction = 0.85  # Ground friction
        self.air_friction = 0.95  # Air friction
        
        # Wall jumping (Hollow Knight style)
        self.wall_slide_speed = 2  # Speed when sliding down walls
        self.wall_jump_force = 12  # Force of wall jump
        self.wall_jump_horizontal_force = 6  # Horizontal force of wall jump
        self.wall_jump_cooldown = 10  # Frames before can wall jump again
        self.wall_jump_timer = 0
        self.wall_sliding = False
        self.wall_direction = 0  # -1 for left wall, 1 for right wall
        
        # Status
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.facing_right = True
        self.health = 100
        self.max_health = 100
        
        # Coyote jump (improved)
        self.coyote_time = COYOTE_TIME
        self.coyote_timer = 0
        self.was_on_ground = False
        self.at_edge = False  # New: Track if player is at edge of platform
        self.was_at_edge = False  # Track edge state from previous frame
        
        # Jump buffer system
        self.jump_buffer_time = 5  # frames to buffer jump input
        self.jump_buffer_timer = 0
        self.jump_pressed = False
        self.jump_just_pressed = False
        
        # Variable jump height (Hollow Knight style)
        self.min_jump_speed = PLAYER_JUMP_STRENGTH * 0.6  # Minimum jump height for variable jumps
        self.is_jumping = False  # Track if we're currently in a jump
        
        # Energy system
        self.energy = MAX_ENERGY
        self.max_energy = MAX_ENERGY
        self.on_energy_tile = False
        self.energy_regen_timer = 0
        
        # Melee attack
        self.melee_damage = MELEE_ATTACK_DAMAGE
        self.melee_range = MELEE_ATTACK_RANGE
        self.melee_cooldown = MELEE_ATTACK_COOLDOWN
        self.last_melee_time = 0
        self.melee_attacking = False
        self.melee_attack_rect = None
        self.melee_visual_timer = 0
        
        # Ranged attack
        self.ranged_damage = RANGED_ATTACK_DAMAGE
        self.ranged_cooldown = RANGED_ATTACK_COOLDOWN
        self.last_ranged_time = 0
        self.ranged_attacking = False
        
        # Elemental abilities
        self.current_region = None
        self.unlocked_abilities = []  # Regional abilities unlocked in current region
        self.permanent_abilities = []  # Abilities that carry between regions
        self.ability_cooldowns = {}
        self.dash_timer = 0
        self.dash_duration = 20  # frames
        
        # Inventory
        self.crystal_fragments = {}  # {region: count}
        self.elemental_crystals = []  # Completed crystals
        
        # Animation
        self.frame_index = 0
        self.animation_speed = 0.15
        
    def set_region(self, region):
        """Set current region and reset regional abilities"""
        self.current_region = region
        self.unlocked_abilities = []  # Reset regional abilities
        
    def unlock_ability(self, ability, permanent=False):
        """Unlock an ability for the player"""
        if permanent:
            if ability not in self.permanent_abilities:
                self.permanent_abilities.append(ability)
        else:
            if ability not in self.unlocked_abilities:
                self.unlocked_abilities.append(ability)
                
    def can_use_ability(self, ability):
        """Check if player can use a specific ability"""
        if ability in self.permanent_abilities:
            return True
        if self.current_region and ability.startswith(self.current_region):
            return ability in self.unlocked_abilities
        return False
        
    def use_ability(self, ability_num):
        """Use an ability based on number (1, 2, or 3)"""
        available_abilities = self.get_available_abilities()
        if ability_num <= len(available_abilities):
            ability = available_abilities[ability_num - 1]
            if self.can_use_ability(ability):
                self.activate_ability(ability)
                
    def get_available_abilities(self):
        """Get list of currently available abilities"""
        abilities = []
        
        # Add permanent abilities first
        abilities.extend(self.permanent_abilities)
        
        # Add regional abilities if in a region
        if self.current_region:
            regional_abilities = [a for a in self.unlocked_abilities 
                                if a.startswith(self.current_region)]
            abilities.extend(regional_abilities)
            
        return abilities[:3]  # Max 3 active abilities
        
    def activate_ability(self, ability):
        """Activate a specific ability"""
        current_time = pygame.time.get_ticks()
        
        # Check cooldown
        if ability in self.ability_cooldowns:
            if current_time - self.ability_cooldowns[ability] < 1000:  # 1 second cooldown
                return
        
        self.ability_cooldowns[ability] = current_time
        
        # Earth abilities
        if ability == 'earth_shield':
            self.create_earth_shield()
        elif ability == 'earth_spike':
            self.create_earth_spike()
        elif ability == 'earth_tunnel':
            self.earth_tunnel()
            
        # Fire abilities
        elif ability == 'fire_dash':
            self.fire_dash()
        elif ability == 'fire_projectile':
            self.fire_projectile()
        elif ability == 'fire_aura':
            self.fire_aura()
            
        # Water abilities  
        elif ability == 'water_heal':
            self.water_heal()
        elif ability == 'water_bubble':
            self.water_bubble()
        elif ability == 'water_flow':
            self.water_flow()
            
        # Air abilities
        elif ability == 'air_jump':
            self.air_jump()
        elif ability == 'air_dash':
            self.air_dash()
        elif ability == 'air_glide':
            self.air_glide()
            
        # Space abilities
        elif ability == 'space_teleport':
            self.space_teleport()
        elif ability == 'space_slow':
            self.space_slow()
        elif ability == 'space_phase':
            self.space_phase()
            
    def create_earth_shield(self):
        """Create protective earth barrier"""
        # TODO: Implement earth shield logic
        print("Earth Shield activated!")
        
    def create_earth_spike(self):
        """Create earth spikes for attack/platform"""
        # TODO: Implement earth spike logic
        print("Earth Spike activated!")
        
    def earth_tunnel(self):
        """Tunnel through earth platforms"""
        # TODO: Implement tunneling logic
        print("Earth Tunnel activated!")
        
    def fire_dash(self):
        """Dash with fire trail"""
        # Stronger dash that lasts longer
        dash_force = 20 if self.facing_right else -20
        self.direction.x = dash_force
        # Add temporary speed boost
        self.speed = PLAYER_SPEED * 3
        self.dash_timer = self.dash_duration
        print("Fire Dash activated!")
        
    def fire_projectile(self):
        """Shoot fire projectile"""
        # TODO: Implement fire projectile
        print("Fire Projectile activated!")
        
    def fire_aura(self):
        """Create damaging fire aura"""
        # TODO: Implement fire aura
        print("Fire Aura activated!")
        
    def water_heal(self):
        """Heal player with water"""
        self.health = min(self.max_health, self.health + 20)
        print("Water Heal activated!")
        
    def water_bubble(self):
        """Create protective water bubble"""
        # TODO: Implement water bubble
        print("Water Bubble activated!")
        
    def water_flow(self):
        """Flow through small spaces"""
        # TODO: Implement water flow
        print("Water Flow activated!")
        
    def air_jump(self):
        """Double/triple jump ability"""
        if not self.on_ground:
            self.direction.y = self.jump_speed * 0.8
        print("Air Jump activated!")
        
    def air_dash(self):
        """Horizontal air dash"""
        if not self.on_ground:
            self.direction.x = 8 if self.facing_right else -8
        print("Air Dash activated!")
        
    def air_glide(self):
        """Slow fall/glide"""
        if self.direction.y > 0:
            self.direction.y *= 0.5
        print("Air Glide activated!")
        
    def space_teleport(self):
        """Short range teleport"""
        teleport_distance = 100
        new_x = self.rect.x + (teleport_distance if self.facing_right else -teleport_distance)
        self.rect.x = max(0, min(new_x, SCREEN_WIDTH - self.rect.width))
        print("Space Teleport activated!")
        
    def space_slow(self):
        """Slow down time/enemies"""
        # TODO: Implement time slow
        print("Space Slow activated!")
        
    def space_phase(self):
        """Phase through platforms briefly"""
        # TODO: Implement phasing
        print("Space Phase activated!")
        
    def collect_fragment(self, region):
        """Collect a crystal fragment"""
        if region not in self.crystal_fragments:
            self.crystal_fragments[region] = 0
        self.crystal_fragments[region] += 1
        
        # Check if crystal is complete
        if self.crystal_fragments[region] >= FRAGMENTS_NEEDED:
            self.complete_crystal(region)
            
    def complete_crystal(self, region):
        """Complete an elemental crystal"""
        if region not in self.elemental_crystals:
            self.elemental_crystals.append(region)
            print(f"Completed {region} crystal!")
            
    def get_input(self):
        """Handle player input with Hollow Knight style controls"""
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Movement with acceleration and friction
        target_speed = 0
        if keys[CONTROLS['move_left']]:
            target_speed = -self.max_speed
            self.facing_right = False
        elif keys[CONTROLS['move_right']]:
            target_speed = self.max_speed
            self.facing_right = True
            
        # Wall sliding detection
        self.wall_sliding = False
        if not self.on_ground and (self.on_left or self.on_right):
            if (keys[CONTROLS['move_left']] and self.on_left) or (keys[CONTROLS['move_right']] and self.on_right):
                self.wall_sliding = True
                self.wall_direction = -1 if self.on_left else 1
                # Limit fall speed when wall sliding
                if self.direction.y > self.wall_slide_speed:
                    self.direction.y = self.wall_slide_speed
                    
        # Apply acceleration
        if self.on_ground:
            # Ground movement
            if abs(target_speed - self.direction.x) > 0.1:
                self.direction.x += (target_speed - self.direction.x) * self.acceleration
            # Apply friction
            self.direction.x *= self.friction
        else:
            # Air movement (reduced control)
            if abs(target_speed - self.direction.x) > 0.1:
                self.direction.x += (target_speed - self.direction.x) * self.acceleration * self.air_control
            # Apply air friction
            self.direction.x *= self.air_friction
            
        # Jump input handling with buffer
        jump_key_pressed = keys[CONTROLS['jump']]
        
        # Detect when jump key is first pressed
        if jump_key_pressed and not self.jump_pressed:
            self.jump_just_pressed = True
            self.jump_buffer_timer = self.jump_buffer_time
        else:
            self.jump_just_pressed = False
            
        self.jump_pressed = jump_key_pressed
        
        # Handle jump with coyote time, buffer, and wall jumping
        if self.jump_just_pressed or self.jump_buffer_timer > 0:
            if self.on_ground or self.coyote_timer > 0:
                self.jump()
                self.jump_buffer_timer = 0  # Clear buffer when jump is executed
            elif self.wall_sliding and self.wall_jump_timer <= 0:
                self.wall_jump()
                self.jump_buffer_timer = 0
                
        # Variable jump height (hold jump for higher jump)
        if self.jump_pressed and self.is_jumping and self.direction.y < 0:
            # Maintain jump velocity while holding jump button
            self.direction.y = max(self.direction.y, self.min_jump_speed)
        elif not self.jump_pressed or self.direction.y >= 0:
            # Reset jump state when not holding jump or when falling
            self.is_jumping = False
            
        # Abilities
        if keys[CONTROLS['ability_1']]:
            self.use_ability(1)
        if keys[CONTROLS['ability_2']]:
            self.use_ability(2)
        if keys[CONTROLS['ability_3']]:
            self.use_ability(3)
            
        # Melee attack
        if mouse_buttons[0]:  # Left mouse button
            self.melee_attack()
            
        # Ranged attack
        if mouse_buttons[2]:  # Right mouse button
            self.ranged_attack()
            
    def melee_attack(self):
        """Perform melee attack"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_melee_time < self.melee_cooldown:
            return
            
        self.last_melee_time = current_time
        
        # Create attack hitbox in front of player
        attack_x = self.rect.right if self.facing_right else self.rect.left - self.melee_range
        self.melee_attack_rect = pygame.Rect(attack_x, self.rect.y, self.melee_range, self.rect.height)
        
        # Store attack info for level to handle
        self.melee_attacking = True
        self.melee_visual_timer = 10  # Show visual for 10 frames
        print("Melee attack!")
        
    def ranged_attack(self):
        """Perform ranged attack"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_ranged_time < self.ranged_cooldown:
            return
            
        # Check energy cost
        if self.energy < RANGED_ATTACK_ENERGY_COST:
            print("Not enough energy for ranged attack!")
            return
            
        self.last_ranged_time = current_time
        self.energy -= RANGED_ATTACK_ENERGY_COST
        
        # Get mouse position for direction
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center_x = self.rect.centerx
        player_center_y = self.rect.centery
        
        # Calculate direction vector
        direction_x = mouse_x - player_center_x
        direction_y = mouse_y - player_center_y
        
        # Create projectile
        projectile = Projectile(
            (player_center_x, player_center_y),
            (direction_x, direction_y),
            self.ranged_damage
        )
        
        # Store projectile for level to handle
        self.ranged_attacking = True
        self.current_projectile = projectile
        print("Ranged attack!")
        
    def update_energy(self):
        """Update energy regeneration"""
        if self.on_energy_tile and self.energy < self.max_energy:
            self.energy_regen_timer += 1
            if self.energy_regen_timer >= ENERGY_REGEN_COOLDOWN:
                self.energy = min(self.max_energy, self.energy + ENERGY_REGEN_RATE)
                self.energy_regen_timer = 0
        else:
            self.energy_regen_timer = 0
            
    def update_coyote_time(self):
        """Update coyote jump timer (classic platformer: always works on leaving ground)"""
        # If we just left the ground (regardless of edge), start coyote timer
        if self.was_on_ground and not self.on_ground:
            self.coyote_timer = self.coyote_time
            print(f"Coyote time activated! Timer: {self.coyote_timer}")
        elif self.on_ground:
            self.coyote_timer = 0
        elif self.coyote_timer > 0:
            self.coyote_timer -= 1
        self.was_on_ground = self.on_ground
        
    def wall_jump(self):
        """Perform wall jump"""
        if self.wall_sliding and self.wall_jump_timer <= 0:
            # Jump away from wall
            self.direction.y = -self.wall_jump_force
            self.direction.x = -self.wall_direction * self.wall_jump_horizontal_force
            
            # Set cooldown
            self.wall_jump_timer = self.wall_jump_cooldown
            
            # Reset wall sliding
            self.wall_sliding = False
            
            print(f"Wall jump! Direction: {self.wall_direction}")
            return True
        return False
        
    def jump(self):
        """Make player jump with proper coyote time handling"""
        # Check if we can jump (on ground or coyote time active)
        if self.on_ground or self.coyote_timer > 0:
            self.direction.y = self.jump_speed
            self.coyote_timer = 0  # Reset coyote timer when jumping
            self.is_jumping = True  # Set jumping state
            
            # Debug info - fix the logic
            coyote_used = not self.on_ground  # If we're not on ground, coyote time was used
            print(f"Jump! Coyote time used: {coyote_used}")
            return True
        return False
        
    def apply_gravity(self):
        """Apply gravity to player"""
        self.direction.y += self.gravity
        if self.direction.y > self.max_fall_speed:
            self.direction.y = self.max_fall_speed
        self.rect.y += int(self.direction.y)
        
    def move_horizontally(self):
        """Move player horizontally"""
        self.rect.x += int(self.direction.x * self.speed)
        
    def update(self):
        """Update player state"""
        self.get_input()
        
        # Update jump buffer timer
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= 1
        
        # Update wall jump timer
        if self.wall_jump_timer > 0:
            self.wall_jump_timer -= 1
        
        # Update energy
        self.update_energy()
        
        # Handle dash timer
        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_timer == 0:
                self.speed = PLAYER_SPEED  # Reset speed after dash
                
        # Handle melee attack visual timer
        if self.melee_visual_timer > 0:
            self.melee_visual_timer -= 1
        
        # Note: Horizontal and vertical movement are now handled by level collision system
        # to ensure proper collision detection and prevent double movement
        # Note: Coyote time is now updated in level.py after collision detection
