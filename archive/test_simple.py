import pygame
import sys

# Simple test to check if basic rendering works
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Test Game")
clock = pygame.time.Clock()

# Simple sprites
player_rect = pygame.Rect(100, 400, 32, 48)
platform_rect = pygame.Rect(0, 600, 1200, 64)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Clear screen
    screen.fill((20, 20, 30))
    
    # Draw simple shapes
    pygame.draw.rect(screen, (255, 255, 255), player_rect)  # White player
    pygame.draw.rect(screen, (100, 100, 100), platform_rect)  # Gray platform
    
    # Draw some text
    font = pygame.font.Font(None, 48)
    text = font.render("TEST - Can you see this?", True, (255, 255, 255))
    screen.blit(text, (100, 100))
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
sys.exit()
