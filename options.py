import pygame
import sys
import os
from sound_manager import set_global_volume, play_select_sound

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GRAY = (160, 160, 160)

# Screen dimensions
WIDTH, HEIGHT = 1280, 720

# Fonts
TEXT_FONT = pygame.font.SysFont("arial", 24)
BUTTON_FONT = pygame.font.SysFont("arial", 28)

# Volume slider settings
slider_width = 400
slider_height = 10
slider_rect = pygame.Rect((WIDTH - slider_width) // 2, 300, slider_width, slider_height)
slider_knob_rect = pygame.Rect(slider_rect.x, slider_rect.y - 10, 20, 30)
is_dragging = False

# Get and save current volume
current_volume = pygame.mixer.music.get_volume()
saved_volume = current_volume

def update_knob_position():
    """Update the knob position based on the current volume"""
    slider_knob_rect.x = slider_rect.x + int(current_volume * (slider_rect.width - slider_knob_rect.width))

def draw_text_centered(screen, text, font, color, y_offset):
    """Draws text centered horizontally on the screen"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def draw_options_menu(screen):
    """Draws the options menu with a volume slider"""
    screen.fill(BLACK)
    
    # Draw "Audio Options" title
    draw_text_centered(screen, "Audio Options", TEXT_FONT, WHITE, -200)
    
    # Draw Volume Slider
    pygame.draw.rect(screen, GRAY, slider_rect)  # Slider line
    pygame.draw.rect(screen, WHITE, slider_knob_rect)  # Knob

    # Draw current volume level as a percentage
    volume_percentage = int(current_volume * 100)
    volume_text = TEXT_FONT.render(f"Volume: {volume_percentage}%", True, WHITE)
    screen.blit(volume_text, (WIDTH // 2 - volume_text.get_width() // 2, slider_rect.y + 40))
    
    # Draw "Go Back" button
    button_text = BUTTON_FONT.render("Go Back", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, 550))
    pygame.draw.rect(screen, BLUE, button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)

    return button_rect

def options_screen(screen):
    global is_dragging, current_volume, saved_volume
    clock = pygame.time.Clock()
    running = True

    # Update knob position based on the current volume
    update_knob_position()

    while running:
        button_rect = draw_options_menu(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if button_rect.collidepoint(event.pos):
                        play_select_sound()
                        saved_volume = current_volume  # Save the volume when going back
                        set_global_volume(saved_volume)  # Ensure global volume is updated
                        return "menu"
                    if slider_knob_rect.collidepoint(event.pos):
                        is_dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False

            if event.type == pygame.MOUSEMOTION and is_dragging:
                # Update the position of the slider knob
                slider_knob_rect.x = min(max(event.pos[0], slider_rect.x), slider_rect.x + slider_rect.width - slider_knob_rect.width)
                # Calculate volume based on knob position
                current_volume = (slider_knob_rect.x - slider_rect.x) / (slider_rect.width - slider_knob_rect.width)
                set_global_volume(current_volume)

        clock.tick(60)  # 60 FPS
