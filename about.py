import pygame
import sys
from sound_manager import play_select_sound
from config import WIDTH, HEIGHT, WHITE, BLACK, BLUE, TEXT_FONT, BUTTON_FONT

def draw_text(screen, text, font, color, y_offset):
    """Draws text centered horizontally."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def about_screen(screen):
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        draw_text(screen, "We are students who love space", TEXT_FONT, WHITE, -60)
        draw_text(screen, "and programming.", TEXT_FONT, WHITE, -30)
        draw_text(screen, "Made by - Nabil and Abdullah", TEXT_FONT, WHITE, 10) 
                
        # Draw "Go Back" button
        button_text = BUTTON_FONT.render("Go Back", True, WHITE)
        button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))
        pygame.draw.rect(screen, BLUE, button_rect.inflate(20, 10))
        screen.blit(button_text, button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    play_select_sound()
                    return "menu"

        clock.tick(60)
