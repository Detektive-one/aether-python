import pygame
from settings import GameState

class GameStateManager:
    """Manages different game states and transitions between them"""
    
    def __init__(self):
        self.current_state = GameState.MENU
        self.previous_state = None
        self.state_data = {}
        
    def change_state(self, new_state, data=None):
        """Change to a new game state with optional data"""
        self.previous_state = self.current_state
        self.current_state = new_state
        if data:
            self.state_data[new_state] = data
            
    def get_state_data(self, state=None):
        """Get data for current state or specified state"""
        state = state or self.current_state
        return self.state_data.get(state, {})
        
    def clear_state_data(self, state=None):
        """Clear data for current state or specified state"""
        state = state or self.current_state
        if state in self.state_data:
            del self.state_data[state]
            
    def go_back(self):
        """Return to previous state"""
        if self.previous_state:
            temp = self.current_state
            self.current_state = self.previous_state
            self.previous_state = temp
