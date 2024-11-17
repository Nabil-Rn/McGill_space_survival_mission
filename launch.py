import pygame
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') 
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from physics import rocket_simulation

# Initialize Pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
pygame.display.set_caption("Rocket Launch Simulation")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Rocket parameters for animation
ROCKET_WIDTH, ROCKET_HEIGHT = 20, 60
rocket_x = SCREEN_WIDTH // 4
rocket_y = SCREEN_HEIGHT - ROCKET_HEIGHT
rocket_velocity = 0


def draw_rocket(screen, y_pos):
    """Draw the rocket at the specified y-position."""
    pygame.draw.rect(screen, WHITE, (rocket_x, y_pos, ROCKET_WIDTH, ROCKET_HEIGHT))


def plot_simulation(screen, times, velocities, altitudes):
    """Plot data using Matplotlib and render it in Pygame."""
    # Create Matplotlib figure and axis
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

    # Draw the Matplotlib figure onto a Pygame surface
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()
    plot_surface = pygame.image.frombuffer(raw_data, canvas.get_width_height(), 'RGBA')
    
    # Blit the Matplotlib plot surface onto the Pygame screen
    plot_x = SCREEN_WIDTH // 2
    plot_y = 0
    screen.blit(plot_surface, (plot_x, plot_y))
    plt.close(fig)  # Close the figure to avoid memory leaks


def launch_screen(screen, selected_items,  dry_mass):
    times, velocities, altitudes, accelerations, remaining_fuels, success = rocket_simulation(dry_mass)

    # Animation variables
    running = True
    clock = pygame.time.Clock()
    index = 0

    while running:
        screen.fill(BLACK)  # Clear screen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rocket animation logic
        if index < len(altitudes):
            rocket_y = SCREEN_HEIGHT - int(altitudes[index] / 100)  # Scale altitude for screen
            rocket_velocity = velocities[index]
            index += 1
        else:
            rocket_velocity = 0

        draw_rocket(screen, rocket_y)

        # Plot Matplotlib graph
        plot_simulation(screen, times[:index], velocities[:index], altitudes[:index])

        # Render success/failure message
        font = pygame.font.Font(None, 36)
        message = "Successful Launch!" if success else "Launch Failed!"
        message_surface = font.render(message, True, WHITE)
        screen.blit(message_surface, (10, 10))

        pygame.display.update()
        clock.tick(30)  # Cap at 30 FPS

    pygame.quit()
