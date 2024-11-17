import pygame
import sys
import os
from sound_manager import play_select_sound, start_background_music
from options import options_screen
from map_options import map_selection_screen
from about import about_screen
from config import WIDTH, HEIGHT, WHITE, YELLOW, FONT

# Initialize pygame
pygame.init()

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Space Survival Mission")

# Load background image and stretch it to fit the screen
background = pygame.image.load(os.path.join("media", "space_earth.jpg"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

menu_items = ["Start", "Options", "About", "Exit"]
selected_item = 0

def draw_menu(screen, selected):
    """Draws the main menu options."""
    screen.blit(background, (0, 0))
    for index, item in enumerate(menu_items):
        color = YELLOW if index == selected else WHITE
        text = FONT.render(item, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100 + index * 60))
    pygame.display.flip()

def main_menu(screen):
    global selected_item
    clock = pygame.time.Clock()
    start_background_music()

    while True:
        draw_menu(screen, selected_item)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for index, item in enumerate(menu_items):
            text_surface = FONT.render(item, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + index * 60))
            
            if text_rect.collidepoint(mouse_x, mouse_y):
                selected_item = index

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                play_select_sound()
                if selected_item == 0:
                    return "map_selection"
                elif selected_item == 1:
                    return "options"
                elif selected_item == 2:
                    return "about"
                elif selected_item == 3:
                    return "exit"
        
        clock.tick(60)

def main():
    current_screen = "menu"
    while current_screen != "exit":
        if current_screen == "menu":
            current_screen = main_menu(screen)
        elif current_screen == "options":
            current_screen = options_screen(screen)
        elif current_screen == "map_selection":
            current_screen = map_selection_screen(screen)
        elif current_screen == "about":
            current_screen = about_screen(screen)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
