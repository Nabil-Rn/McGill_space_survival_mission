import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Load the selection sound
select_sound = pygame.mixer.Sound(os.path.join("media", "select.wav"))

# Default volume
current_volume = 0.5

def play_select_sound():
    """Function to play the selection sound"""
    select_sound.play()

def set_sound_volume(volume):
    """Adjust the volume of all sound effects"""
    select_sound.set_volume(volume)

def start_background_music():
    """Function to start playing background music in a loop"""
    pygame.mixer.music.load(os.path.join("media", "background_music.mp3"))
    pygame.mixer.music.set_volume(current_volume)
    pygame.mixer.music.play(-1)  # Loop indefinitely

def set_music_volume(volume):
    """Adjust the volume of the background music"""
    pygame.mixer.music.set_volume(volume)

def set_global_volume(volume):
    """Set the volume for both music and sound effects"""
    global current_volume
    current_volume = volume  # Update the global volume state
    set_music_volume(volume)
    set_sound_volume(volume)

def stop_background_music():
    """Function to stop the background music"""
    pygame.mixer.music.stop()
