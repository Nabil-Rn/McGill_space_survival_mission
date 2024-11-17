import pygame
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') 
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from physics import rocket_simulation
from landing import landing_screen 

# Initialize Pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
pygame.display.set_caption("Rocket Launch Simulation")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT_COLOR = (0, 255, 0)  # Green for button highlight

# Rocket parameters for animation
ROCKET_WIDTH, ROCKET_HEIGHT = 20, 60
rocket_x = SCREEN_WIDTH // 4
rocket_y = SCREEN_HEIGHT - ROCKET_HEIGHT


def draw_rocket(screen, y_pos):
    """Draw the rocket at the specified y-position."""
    pygame.draw.rect(screen, WHITE, (rocket_x, y_pos, ROCKET_WIDTH, ROCKET_HEIGHT))


def plot_simulation(screen, times, velocities, altitudes):
    """Plot data using Matplotlib and render it in Pygame."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 6))
    fig.tight_layout(pad=3.0)
    
    ax1.plot(times, velocities, color='blue')
    ax1.set_title("Velocity over Time")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Velocity (m/s)")
    
    ax2.plot(times, altitudes, color='green')
    ax2.set_title("Altitude over Time")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Altitude (m)")

    canvas = FigureCanvas(fig)
    canvas.draw()
    raw_data = canvas.get_renderer().buffer_rgba()
    plot_surface = pygame.image.frombuffer(raw_data, canvas.get_width_height(), 'RGBA')
    
    screen.blit(plot_surface, (SCREEN_WIDTH // 2, 0))
    plt.close(fig)


def launch_screen(screen, selected_items, dry_mass):
    times, velocities, altitudes, accelerations, remaining_fuels, success = rocket_simulation(dry_mass)

    # Animation variables
    running = True
    clock = pygame.time.Clock()
    index = 0
    font = pygame.font.Font(None, 36)

    # Button configuration
    button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, 120, 40)

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check if the "Next" button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    # Go to the landing screen
                    landing_screen(screen, selected_items)
                    return

        # Rocket animation
        if index < len(altitudes):
            rocket_y = SCREEN_HEIGHT - int(altitudes[index] / 100)
            index += 1
        
        draw_rocket(screen, rocket_y)
        plot_simulation(screen, times[:index], velocities[:index], altitudes[:index])

        # Display success/failure message
        message = "Successful Launch!" if success else "Launch Failed!"
        message_surface = font.render(message, True, WHITE)
        screen.blit(message_surface, (10, 10))

        # Draw the "Next" button
        pygame.draw.rect(screen, WHITE, button_rect, border_radius=5)
        button_text = font.render("Next", True, BLACK)
        screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, 
                                  button_rect.centery - button_text.get_height() // 2))

        # Highlight the button when hovered
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, button_rect, width=3, border_radius=5)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
