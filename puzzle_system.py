import pygame
from settings import *

class PuzzleElement(pygame.sprite.Sprite):
    """Base class for puzzle elements"""
    def __init__(self, pos, element_type, size=(32, 32)):
        super().__init__()
        self.element_type = element_type
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.activated = False
        self.interactable = True
        
    def update(self):
        pass
        
    def interact(self, player):
        """Handle player interaction"""
        pass

class ElementalSwitch(PuzzleElement):
    """Switch that can be activated by specific elements"""
    def __init__(self, pos, required_element, size=(32, 32)):
        super().__init__(pos, required_element, size)
        self.required_element = required_element
        self.image.fill(COLORS.get(required_element, (100, 100, 100)))
        
    def interact(self, player):
        """Check if player has the required element"""
        if player.current_region == self.required_element:
            self.activated = True
            self.image.fill((0, 255, 0))  # Green when activated
            return True
        return False

class ElementalGate(PuzzleElement):
    """Gate that opens when all switches are activated"""
    def __init__(self, pos, switches, size=(64, 64)):
        super().__init__(pos, 'gate', size)
        self.switches = switches
        self.image.fill((150, 150, 150))
        self.open = False
        
    def update(self):
        """Check if all switches are activated"""
        if all(switch.activated for switch in self.switches):
            self.open = True
            self.image.fill((0, 255, 0))  # Green when open
        else:
            self.open = False
            self.image.fill((150, 150, 150))  # Gray when closed

class ElementalCrystal(PuzzleElement):
    """Crystal that needs to be charged with specific elements"""
    def __init__(self, pos, required_charge, size=(48, 48)):
        super().__init__(pos, 'crystal', size)
        self.required_charge = required_charge
        self.current_charge = 0
        self.image.fill(COLORS['crystal_fragment'])
        
    def charge(self, element):
        """Charge the crystal with an element"""
        if element in self.required_charge:
            self.current_charge += 1
            if self.current_charge >= len(self.required_charge):
                self.activated = True
                self.image.fill((0, 255, 255))  # Cyan when fully charged
                return True
        return False

class PuzzleManager:
    """Manages all puzzles in a level"""
    def __init__(self):
        self.puzzles = []
        self.completed_puzzles = []
        
    def add_puzzle(self, puzzle):
        """Add a puzzle to the manager"""
        self.puzzles.append(puzzle)
        
    def update(self, player):
        """Update all puzzles"""
        for puzzle in self.puzzles:
            puzzle.update()
            
    def check_completion(self):
        """Check if all puzzles are completed"""
        return all(puzzle.activated for puzzle in self.puzzles)
        
    def get_puzzle_elements(self):
        """Get all puzzle elements for drawing"""
        return self.puzzles

# Element-specific puzzle types
class FirePuzzle:
    """Fire region specific puzzles"""
    @staticmethod
    def create_melt_ice_puzzle(pos):
        """Create a puzzle where fire melts ice"""
        # TODO: Implement ice melting puzzle
        pass
        
    @staticmethod
    def create_fire_trail_puzzle(pos):
        """Create a puzzle where fire trail lights torches"""
        # TODO: Implement fire trail puzzle
        pass

class WaterPuzzle:
    """Water region specific puzzles"""
    @staticmethod
    def create_water_flow_puzzle(pos):
        """Create a puzzle where water flows to fill containers"""
        # TODO: Implement water flow puzzle
        pass
        
    @staticmethod
    def create_water_pressure_puzzle(pos):
        """Create a puzzle using water pressure"""
        # TODO: Implement water pressure puzzle
        pass

class AirPuzzle:
    """Air region specific puzzles"""
    @staticmethod
    def create_wind_puzzle(pos):
        """Create a puzzle using wind currents"""
        # TODO: Implement wind puzzle
        pass
        
    @staticmethod
    def create_air_lift_puzzle(pos):
        """Create a puzzle using air lifts"""
        # TODO: Implement air lift puzzle
        pass

class EarthPuzzle:
    """Earth region specific puzzles"""
    @staticmethod
    def create_earth_platform_puzzle(pos):
        """Create a puzzle using earth platforms"""
        # TODO: Implement earth platform puzzle
        pass
        
    @staticmethod
    def create_earth_tunnel_puzzle(pos):
        """Create a puzzle using earth tunneling"""
        # TODO: Implement earth tunnel puzzle
        pass

class SpacePuzzle:
    """Space region specific puzzles"""
    @staticmethod
    def create_gravity_puzzle(pos):
        """Create a puzzle using gravity manipulation"""
        # TODO: Implement gravity puzzle
        pass
        
    @staticmethod
    def create_teleport_puzzle(pos):
        """Create a puzzle using teleportation"""
        # TODO: Implement teleport puzzle
        pass
