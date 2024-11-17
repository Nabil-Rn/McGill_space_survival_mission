import pygame
import sys
from config import WIDTH, HEIGHT

# NASA's ranking of items (1 is the highest priority)
nasa_ranking = {
    "Two 100 lb. tanks of oxygen": 1,
    "20 liters of water": 2,
    "Stellar map": 3,
    "Food concentrate": 4,
    "Solar-powered FM receiver-transmitter": 5,
    "50 feet of nylon rope": 6,
    "First aid kit, including injection needle": 7,
    "Parachute silk": 8,
    "Self-inflating life raft": 9,
    "Signal flares": 10,
    "Two .45 caliber pistols": 11,
    "One case of dehydrated milk": 12,
    "Portable heating unit": 13,
    "Magnetic compass": 14,
    "Box of matches": 15
}

def calculate_score(selected_items):
    """Calculate the score based on difference from NASA ranking."""
    total_score = 0
    for index, item in enumerate(selected_items):
        if item in nasa_ranking:
            total_score += abs(nasa_ranking[item] - (index + 1))
    return total_score

def get_rating_and_stars(score):
    """Determine rating and number of stars based on the score."""
    if score <= 25:
        return "Excellent", 6
    elif score <= 32:
        return "Good", 5
    elif score <= 45:
        return "Average", 4
    elif score <= 55:
        return "Fair", 3
    elif score <= 70:
        return "Poor", 2
    else:
        return "Very Poor", 1

def draw_stars(screen, num_stars, star_image):
    """Draw stars on the screen based on the rating."""
    star_width = 50
    star_spacing = 10
    start_x = (WIDTH - (num_stars * (star_width + star_spacing) - star_spacing)) // 2
    y_pos = 250

    for i in range(num_stars):
        screen.blit(star_image, (start_x + i * (star_width + star_spacing), y_pos))

def landing_screen(screen, selected_items):
    pygame.init()
    font = pygame.font.Font(None, 48)

    # Load the background image
    moon_bg = pygame.image.load("media/moon.jpg")
    moon_bg = pygame.transform.scale(moon_bg, (WIDTH, HEIGHT))

    # Load the star image
    star_image = pygame.image.load("media/star.png")
    star_image = pygame.transform.scale(star_image, (50, 50))

    # Calculate score and rating
    score = calculate_score(selected_items)
    rating, num_stars = get_rating_and_stars(score)

    # Button configuration
    exit_button_rect = pygame.Rect(50, HEIGHT - 70, 100, 40)
    running = True

    while running:
        screen.blit(moon_bg, (0, 0))  # Set background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check if the "Exit" button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()  # Exit the program

        # Display "Survival Rating" title
        title_surface = font.render("Survival Rating", True, (255, 255, 255))
        screen.blit(title_surface, ((WIDTH - title_surface.get_width()) // 2, 50))

        # Display score and rating
        score_text = f"Your Score: {score}"
        rating_text = f"Rating: {rating}"

        score_surface = font.render(score_text, True, (255, 255, 255))
        rating_surface = font.render(rating_text, True, (255, 255, 255))

        screen.blit(score_surface, ((WIDTH - score_surface.get_width()) // 2, 150))
        screen.blit(rating_surface, ((WIDTH - rating_surface.get_width()) // 2, 200))

        # Draw stars based on rating
        draw_stars(screen, num_stars, star_image)

        # Draw the "Exit" button
        pygame.draw.rect(screen, (255, 255, 255), exit_button_rect, border_radius=5)
        exit_text = font.render("Exit", True, (0, 0, 0))
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2,
                                exit_button_rect.centery - exit_text.get_height() // 2))

        pygame.display.update()

    pygame.quit()
    sys.exit()
