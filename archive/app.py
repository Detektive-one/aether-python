import pygame
import sys
from settings import *
from game_state_manager import GameStateManager
from level import Level

class Game:
    """Main game class handling different states and the game loop"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Elemental Metroidvania")
        self.clock = pygame.time.Clock()
        
        # Game state management
        self.state_manager = GameStateManager()
        
        # Game objects
        self.current_level = None
        
        # Input handling
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        
    def handle_events(self):
        """Handle pygame events"""
        self.keys_just_pressed.clear()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key not in self.keys_pressed:
                    self.keys_just_pressed.add(event.key)
                self.keys_pressed.add(event.key)
                
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                
        return True
        
    def update_menu(self):
        """Update menu state"""
        if pygame.K_RETURN in self.keys_just_pressed:
            self.state_manager.change_state(GameState.PLAYING)
            self.current_level = Level(self.screen)
            
        if pygame.K_ESCAPE in self.keys_just_pressed:
            return False
            
        return True
        
    def update_playing(self):
        """Update playing state"""
        if pygame.K_ESCAPE in self.keys_just_pressed:
            self.state_manager.change_state(GameState.PAUSED)
            
        if self.current_level:
            # Update level logic only, don't draw yet
            self.current_level.update()
            
            # Check if player died
            if self.current_level.player.sprite and self.current_level.player.sprite.health <= 0:
                print("💀 Player died! Health reached zero.")
                self.state_manager.change_state(GameState.GAME_OVER)
                
            # Check if level is complete
            if self.current_level.boss.sprite and self.current_level.boss.sprite.health <= 0:
                self.state_manager.change_state(GameState.VICTORY)
                
        return True
        
    def update_paused(self):
        """Update paused state"""
        if pygame.K_ESCAPE in self.keys_just_pressed:
            self.state_manager.change_state(GameState.PLAYING)
            
        return True
        
    def update_game_over(self):
        """Update game over state"""
        if pygame.K_RETURN in self.keys_just_pressed:
            # Restart the level
            self.current_level = Level(self.screen)
            self.state_manager.change_state(GameState.PLAYING)
            
        if pygame.K_ESCAPE in self.keys_just_pressed:
            return False
            
        return True
        
    def update_victory(self):
        """Update victory state"""
        if pygame.K_RETURN in self.keys_just_pressed:
            self.state_manager.change_state(GameState.MENU)
            self.current_level = None
            
        if pygame.K_ESCAPE in self.keys_just_pressed:
            return False
            
        return True
        
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(COLORS['background'])
        
        # Title
        font_large = pygame.font.Font(None, 72)
        title = font_large.render("Elemental Metroidvania", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title, title_rect)
        
        # Instructions
        font_medium = pygame.font.Font(None, 48)
        start_text = font_medium.render("Press ENTER to Start Tutorial", True, (200, 200, 200))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        quit_text = font_medium.render("Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(quit_text, quit_rect)
        
        # Controls
        font_small = pygame.font.Font(None, 36)
        controls = [
            "Controls:",
            "WASD - Move",
            "Space - Jump", 
            "Q, E, R - Abilities",
            "Left Click - Attack",
            "ESC - Pause"
        ]
        
        for i, control in enumerate(controls):
            text = font_small.render(control, True, (150, 150, 150))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150 + i * 30))
            self.screen.blit(text, text_rect)
            
    def draw_playing(self):
        """Draw playing state"""
        self.screen.fill(COLORS['background'])
        # Draw the level
        if self.current_level:
            self.current_level.draw()
        
    def draw_paused(self):
        """Draw paused state"""
        # Draw current level first
        self.draw_playing()
        
        # Overlay pause menu
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        font_small = pygame.font.Font(None, 48)
        resume_text = font_small.render("Press ESC to Resume", True, (200, 200, 200))
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(resume_text, resume_rect)
        
    def draw_game_over(self):
        """Draw game over state"""
        self.screen.fill((50, 0, 0))  # Dark red background
        
        font_large = pygame.font.Font(None, 72)
        game_over_text = font_large.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        font_medium = pygame.font.Font(None, 36)
        death_text = font_medium.render("Your health reached zero!", True, (255, 150, 150))
        death_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(death_text, death_rect)
        
        tip_text = font_medium.render("Tip: Use left click to attack enemies and avoid lava!", True, (200, 200, 200))
        tip_rect = tip_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(tip_text, tip_rect)
        
        font_medium = pygame.font.Font(None, 48)
        restart_text = font_medium.render("Press ENTER to Try Again", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = font_medium.render("Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(quit_text, quit_rect)
        
    def draw_victory(self):
        """Draw victory state"""
        self.screen.fill((0, 50, 0))  # Dark green background
        
        font_large = pygame.font.Font(None, 72)
        victory_text = font_large.render("TUTORIAL COMPLETE!", True, (100, 255, 100))
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        font_medium = pygame.font.Font(None, 48)
        continue_text = font_medium.render("You've mastered the basics!", True, (200, 255, 200))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(continue_text, continue_rect)
        
        restart_text = font_medium.render("Press ENTER to Return to Menu", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = font_medium.render("Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(quit_text, quit_rect)
        
    def update(self):
        """Update game based on current state"""
        current_state = self.state_manager.current_state
        
        if current_state == GameState.MENU:
            return self.update_menu()
        elif current_state == GameState.PLAYING:
            return self.update_playing()
        elif current_state == GameState.PAUSED:
            return self.update_paused()
        elif current_state == GameState.GAME_OVER:
            return self.update_game_over()
        elif current_state == GameState.VICTORY:
            return self.update_victory()
            
        return True
        
    def draw(self):
        """Draw game based on current state"""
        current_state = self.state_manager.current_state
        
        if current_state == GameState.MENU:
            self.draw_menu()
        elif current_state == GameState.PLAYING:
            self.draw_playing()
        elif current_state == GameState.PAUSED:
            self.draw_paused()
        elif current_state == GameState.GAME_OVER:
            self.draw_game_over()
        elif current_state == GameState.VICTORY:
            self.draw_victory()
            
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            if not running:
                break
                
            # Update game
            running = self.update()
            if not running:
                break
                
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
