import pygame
from game import Game

def main():
    pygame.init()
    # Set up the screen
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Asteroid Game")

    clock = pygame.time.Clock()
    running = True

    # Create a Game instance
