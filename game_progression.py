import json
import os
from settings import *

class GameProgression:
    """Manages game progression, save/load, and region completion"""
    
    def __init__(self):
        self.save_file = "game_save.json"
        self.current_region = 'fire'
        self.completed_regions = []
        self.unlocked_abilities = {
            'fire': [],
            'water': [],
            'earth': [],
            'air': [],
            'space': []
        }
        self.permanent_abilities = []
        self.crystal_fragments = {
            'fire': 0,
            'water': 0,
            'earth': 0,
            'air': 0,
            'space': 0
        }
        self.completed_crystals = []
        self.current_level = 1
        self.hidden_levels_completed = []
        self.bosses_defeated = []
        
    def save_game(self):
        """Save current game state to file"""
        save_data = {
            'current_region': self.current_region,
            'completed_regions': self.completed_regions,
            'unlocked_abilities': self.unlocked_abilities,
            'permanent_abilities': self.permanent_abilities,
            'crystal_fragments': self.crystal_fragments,
            'completed_crystals': self.completed_crystals,
            'current_level': self.current_level,
            'hidden_levels_completed': self.hidden_levels_completed,
            'bosses_defeated': self.bosses_defeated
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            print("Game saved successfully!")
        except Exception as e:
            print(f"Error saving game: {e}")
            
    def load_game(self):
        """Load game state from file"""
        if not os.path.exists(self.save_file):
            print("No save file found. Starting new game.")
            return False
            
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
                
            self.current_region = save_data.get('current_region', 'fire')
            self.completed_regions = save_data.get('completed_regions', [])
            self.unlocked_abilities = save_data.get('unlocked_abilities', {
                'fire': [], 'water': [], 'earth': [], 'air': [], 'space': []
            })
            self.permanent_abilities = save_data.get('permanent_abilities', [])
            self.crystal_fragments = save_data.get('crystal_fragments', {
                'fire': 0, 'water': 0, 'earth': 0, 'air': 0, 'space': 0
            })
            self.completed_crystals = save_data.get('completed_crystals', [])
            self.current_level = save_data.get('current_level', 1)
            self.hidden_levels_completed = save_data.get('hidden_levels_completed', [])
            self.bosses_defeated = save_data.get('bosses_defeated', [])
            
            print("Game loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
            
    def unlock_ability(self, region, ability, permanent=False):
        """Unlock an ability for a specific region"""
        if permanent:
            if ability not in self.permanent_abilities:
                self.permanent_abilities.append(ability)
                print(f"Permanent ability unlocked: {ability}")
        else:
            if ability not in self.unlocked_abilities[region]:
                self.unlocked_abilities[region].append(ability)
                print(f"Regional ability unlocked: {ability} in {region}")
                
    def collect_fragment(self, region):
        """Collect a crystal fragment"""
        self.crystal_fragments[region] += 1
        print(f"Collected {region} fragment! ({self.crystal_fragments[region]}/{FRAGMENTS_NEEDED})")
        
        # Check if crystal is complete
        if self.crystal_fragments[region] >= FRAGMENTS_NEEDED:
            self.complete_crystal(region)
            
    def complete_crystal(self, region):
        """Complete an elemental crystal"""
        if region not in self.completed_crystals:
            self.completed_crystals.append(region)
            print(f"Completed {region} crystal!")
            
    def complete_region(self, region):
        """Mark a region as completed"""
        if region not in self.completed_regions:
            self.completed_regions.append(region)
            print(f"Region {region} completed!")
            
    def get_available_abilities(self, region):
        """Get all available abilities for current region"""
        abilities = []
        
        # Add permanent abilities
        abilities.extend(self.permanent_abilities)
        
        # Add regional abilities
        abilities.extend(self.unlocked_abilities[region])
        
        return abilities[:3]  # Max 3 active abilities
        
    def can_access_region(self, region):
        """Check if player can access a region"""
        # For now, allow access to adjacent regions
        # Later, implement proper region unlocking logic
        return True
        
    def get_region_difficulty(self, region):
        """Get difficulty modifier for a region based on starting region"""
        if not self.completed_regions:
            return 1.0  # Normal difficulty for starting region
            
        # Calculate difficulty based on elemental relationships
        starting_region = self.completed_regions[0] if self.completed_regions else 'fire'
        
        # Regions that are opposites are easier
        if region in ELEMENT_WEAKNESSES.get(starting_region, []):
            return 0.7  # Easier
        elif starting_region in ELEMENT_WEAKNESSES.get(region, []):
            return 1.3  # Harder
        else:
            return 1.0  # Normal
            
    def get_next_region(self):
        """Get the next region to unlock"""
        if not self.completed_regions:
            return 'fire'
            
        # Simple progression: fire -> water -> earth -> air -> space
        region_order = ['fire', 'water', 'earth', 'air', 'space']
        current_index = region_order.index(self.current_region)
        
        if current_index < len(region_order) - 1:
            return region_order[current_index + 1]
        return None
        
    def reset_game(self):
        """Reset all progression data"""
        self.current_region = 'fire'
        self.completed_regions = []
        self.unlocked_abilities = {
            'fire': [], 'water': [], 'earth': [], 'air': [], 'space': []
        }
        self.permanent_abilities = []
        self.crystal_fragments = {
            'fire': 0, 'water': 0, 'earth': 0, 'air': 0, 'space': 0
        }
        self.completed_crystals = []
        self.current_level = 1
        self.hidden_levels_completed = []
        self.bosses_defeated = []
        
        # Delete save file
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
            
        print("Game reset successfully!")
