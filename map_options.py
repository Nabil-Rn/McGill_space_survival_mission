import pygame
import sys
import os
import random
from sound_manager import play_select_sound
from equipment import equipment_screen
from config import WIDTH, HEIGHT, WHITE, TEXT_FONT

# Load images for the maps
moon_img = pygame.image.load(os.path.join("media", "moon.jpg"))
mars_img = pygame.image.load(os.path.join("media", "mars.jpg"))
hidden_img = pygame.image.load(os.path.join("media", "hidden.jpg"))

# Scale images proportionally to fit within 250x250 without stretching
moon_img = pygame.transform.scale(moon_img, (250, 250))
mars_img = pygame.transform.scale(mars_img, (250, 250))
hidden_img = pygame.transform.scale(hidden_img, (250, 250))

# Updated positions for the larger screen
buttons = [
    {"name": "Moon", "image": moon_img, "pos": (WIDTH // 4, HEIGHT // 2)},
    {"name": "Mars", "image": mars_img, "pos": (WIDTH // 2, HEIGHT // 2)},
    {"name": "Hidden", "image": hidden_img, "pos": (3 * WIDTH // 4, HEIGHT // 2)}
]

# Create a list of stars with random positions and speeds
stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "speed": random.uniform(0.1, 0.5)} for _ in range(100)]

def update_stars():
    """Update the position of stars to create a slow-moving effect."""
    for star in stars:
        star["y"] += star["speed"]
        # If the star goes off the screen, reset its position
        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

def draw_stars(screen):
    """Draw slow-moving stars on the background."""
    for star in stars:
        pygame.draw.circle(screen, WHITE, (int(star["x"]), int(star["y"])), 2)

def draw_map_options(screen):
    """Draws the map selection screen"""
    screen.fill((0, 0, 0))  # Black background
    
    # Draw moving stars in the background
    draw_stars(screen)
    
    # Draw each map button
    for button in buttons:
        img = button["image"]
        pos = button["pos"]
        img_rect = img.get_rect(center=pos)
        screen.blit(img, img_rect)

        # Draw map name below each image
        label = TEXT_FONT.render(button["name"], True, WHITE)
        label_rect = label.get_rect(center=(pos[0], pos[1] + img_rect.height // 2 + 30))
        screen.blit(label, label_rect)

    pygame.display.flip()

def map_selection_screen(screen):
    clock = pygame.time.Clock()
    running = True

    while running:
        update_stars()  # Update the stars positions
        draw_map_options(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in buttons:
                    img_rect = button["image"].get_rect(center=button["pos"])
                    if img_rect.collidepoint(mouse_pos):
                        play_select_sound()
                        equipment_screen(button["name"])
                        return "menu"

        clock.tick(60)

    return "menu"
