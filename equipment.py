import pygame
import sys
import os
import random
from sound_manager import play_select_sound
from config import WIDTH, HEIGHT, WHITE, BLACK, HIGHLIGHT_COLOR
from launch import launch_screen

# Screen dimensions
WIDTH, HEIGHT = 1280, 720  # Updated to 1280x720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Equipment Selection")

# Fonts
pygame.font.init()
TEXT_FONT = pygame.font.SysFont("arial", 16)

# Load space background and scale it
background = pygame.image.load(os.path.join("media", "space_earth.jpg"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

total_weight = 0.0

# Equipment map with weights
equipment_map = {
    "Box of matches": 0.1,
    "Food concentrate": 2.0,
    "50 feet of nylon rope": 1.5,
    "Parachute silk": 1.0,
    "Portable heating unit": 3.5,
    "Two .45 caliber pistols": 1.2,
    "One case of dehydrated milk": 5.0,
    "Two 100 lb. tanks of oxygen": 90.7,
    "Stellar map": 0.3,
    "Self-inflating life raft": 6.0,
    "Magnetic compass": 0.2,
    "20 liters of water": 20.0,
    "Signal flares": 0.5,
    "First aid kit, including injection needle": 1.0,
    "Solar-powered FM receiver-transmitter": 0.8,
}

# Equipment buttons positions and states
buttons = []
dragging_item = None
drag_offset = (0, 0)
scroll_offset = 0  # Vertical offset for scroll

# Selected items
selected_items = []
# max_selected_items = 5  # Limit the number of selected items
# max_weight = 50.0  # Maximum weight limit in kg

# Generate random stars for the background
stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "speed": random.uniform(0.1, 0.5)} for _ in range(100)]

def update_stars():
    """Update the position of stars to create a slow-moving effect."""
    for star in stars:
        star["y"] += star["speed"]
        # If the star goes off the screen, reset its position
        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

def draw_stars():
    """Draw random white stars on the background."""
    for star in stars:
        pygame.draw.circle(screen, WHITE, (int(star["x"]), int(star["y"])), 2)

def draw_welcome_message(map_name):
    """Draw the welcome message in the left third of the screen with a black background behind it."""
    welcome_text = (
        f"Welcome to the {map_name} mission!"
        "Here you need to select the items that you will need!"
        "while you are picking them, order them in what you think the most important!"
        "Remember you can select as much as you want but be warned you could not launch successfully"
        "Reas you could add too much or too little !"
    )
    # f"only {max_selected_items} items to be able to fly. The better items you get, "
    #     "the better for survival! Total weight limit is {max_weight} kg."

    wrapped_text = wrap_text(welcome_text, WIDTH // 3 - 20)  # Wrap text to fit left third of screen

    # Calculate the total height of the wrapped text
    total_text_height = len(wrapped_text) * (TEXT_FONT.get_height() + 5) + 10 

    # Position of the black rectangle background (left-aligned and with the same width)
    background_rect = pygame.Rect(10, 100, WIDTH // 3 - 20, total_text_height)
    pygame.draw.rect(screen, BLACK, background_rect)  # Draw black background behind the text

    # Now draw the wrapped text on top of the black rectangle
    y_offset = 100
    for line in wrapped_text:
        label = TEXT_FONT.render(line, True, WHITE)
        screen.blit(label, (20, y_offset))  # Position text with some padding from the left
        y_offset += TEXT_FONT.get_height() + 5  # Line height plus padding


def wrap_text(text, max_width):
    """Wraps text to fit inside a given width."""
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        test_label = TEXT_FONT.render(test_line, True, WHITE)
        
        if test_label.get_width() <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

def draw_equipment_buttons():
    """Draw the equipment buttons in the right third of the screen with hover effect."""
    global buttons
    buttons = []  # Reset buttons to avoid duplicates
    button_width = WIDTH // 3 - 20
    for i, item in enumerate(equipment_map.keys()):
        button_rect = pygame.Rect(WIDTH * 2 // 3 + 10, 10 + (i * 40) - scroll_offset, button_width, 30)
        buttons.append({"name": item, "rect": button_rect, "dragged": False})
        
        # Draw the button background (black)
        pygame.draw.rect(screen, BLACK, button_rect, border_radius=5)
        
        # Wrap the text inside the button
        wrapped_text = wrap_text(item, button_rect.width - 20)
        for j, line in enumerate(wrapped_text):
            label = TEXT_FONT.render(line, True, WHITE)
            label_rect = label.get_rect(center=button_rect.center)
            label_rect.y += j * TEXT_FONT.get_height()
            screen.blit(label, label_rect)
        
        # Highlight the button when hovered
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, button_rect, width=2, border_radius=5)

def draw_order_panel(total_weight):
    """Draws the order panel in the middle third of the screen."""
    panel_x = WIDTH // 3
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(panel_x, 0, panel_x, HEIGHT))  # Full middle panel

    y_offset = 10
    total_weight = 0  # Initialize the total weight

    for idx, item in enumerate(selected_items):
        weight = equipment_map[item]
        total_weight += weight
        item_text = f"{idx + 1}. {item} ({weight} kg)"  # Add number before each item
        label = TEXT_FONT.render(item_text, True, WHITE)
        screen.blit(label, (panel_x + 10, y_offset))
        y_offset += 40  # Increase space between items

    # Display total weight at the bottom of the list
    total_weight_text = f"Total Weight: {total_weight:.2f} kg"
    total_weight_surface = TEXT_FONT.render(total_weight_text, True, WHITE)
    screen.blit(total_weight_surface, (panel_x + 10, y_offset + 10))


def handle_dragging(event):
    """Handles the dragging of equipment items."""
    global dragging_item, drag_offset
    if dragging_item is not None:
        mouse_x, mouse_y = event.pos
        dragging_item['rect'].x = mouse_x - drag_offset[0]
        dragging_item['rect'].y = mouse_y - drag_offset[1]

def start_drag(event):
    """Starts dragging an item from the selected items in the order panel."""
    global dragging_item, drag_offset
    mouse_x, mouse_y = event.pos
    for idx, item in enumerate(selected_items):
        item_rect = pygame.Rect(WIDTH // 3 + 10, 10 + idx * 40, WIDTH // 3 - 20, 30)
        if item_rect.collidepoint(mouse_x, mouse_y):
            dragging_item = {"name": item, "index": idx}  # Store index for reorder
            drag_offset = (mouse_x - item_rect.x, mouse_y - item_rect.y)
            break

def handle_dragging(event):
    """Handles the dragging of selected items within the order panel."""
    global dragging_item, drag_offset
    if dragging_item:
        mouse_x, mouse_y = event.pos
        item_index = dragging_item["index"]
        
        # Calculate new position
        new_position = (mouse_y - 10) // 40
        new_position = max(0, min(new_position, len(selected_items) - 1))
        
        # Reorder if the new position is different
        if new_position != item_index:
            selected_items.insert(new_position, selected_items.pop(item_index))
            dragging_item["index"] = new_position  # Update the index of the dragged item

def stop_drag():
    """Stops dragging and resets the dragging item."""
    global dragging_item
    dragging_item = None  # Reset dragging item

def scroll_list(event):
    """Handles scrolling of the equipment list."""
    global scroll_offset
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Scroll up
        scroll_offset = max(0, scroll_offset - 10)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Scroll down
        scroll_offset += 10

def handle_item_selection(event):
    """Handle equipment item selection by mouse click."""
    mouse_x, mouse_y = event.pos
    for button in buttons:
        if button["rect"].collidepoint(mouse_x, mouse_y):
            item = button["name"]
            weight = equipment_map[item]
            total_weight = sum(equipment_map[selected_item] for selected_item in selected_items)
            
            if item not in selected_items:
                selected_items.append(item)
                play_select_sound()
                # if len(selected_items) < max_selected_items and total_weight + weight <= max_weight:
                #     selected_items.append(item)
                #     play_select_sound()
                # elif len(selected_items) >= max_selected_items:
                #     print("You have reached the maximum number of items.")
                # elif total_weight + weight > max_weight:
                #     print("Adding this item would exceed the weight limit.")
            elif item in selected_items:
                selected_items.remove(item)
                play_select_sound()
            break

# def launch_screen(selected_items):
#     """Transition to the launch screen with the selected items in order."""
#     print("Launching mission with the following items in order:")
#     for item in selected_items:
#         print(item)
#     # Additional code to transition to the new screen (visuals, etc.)

def equipment_screen(map_name):
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(background, (0, 0))  # Draw space background with stars
        update_stars()  # Update star positions
        draw_stars()  # Draw stars
        draw_welcome_message(map_name)  # Draw welcome message in left third
        draw_equipment_buttons()  # Draw the equipment buttons
        draw_order_panel(total_weight)  # Draw the order panel

        # Draw the Launch button in the bottom-right corner
        launch_button_rect = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, launch_button_rect, border_radius=5)
        launch_text = TEXT_FONT.render("Launch", True, BLACK)
        screen.blit(launch_text, (launch_button_rect.centerx - launch_text.get_width() // 2, launch_button_rect.centery - launch_text.get_height() // 2))
        
        if launch_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, WHITE, launch_button_rect, width=3)
            if pygame.mouse.get_pressed()[0]:  # Left click
                launch_screen(screen, selected_items, total_weight)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_drag(event)
                handle_item_selection(event)

            if event.type == pygame.MOUSEMOTION:
                if dragging_item is not None:
                    handle_dragging(event)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                stop_drag()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()

            scroll_list(event)  # Handle scroll events

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

if __name__ == "__main__":
    equipment_screen("Moon")
    pygame.quit()
