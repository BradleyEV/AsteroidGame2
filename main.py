import pygame
from game import GameState, Game

def main():
    print("Initializing pygame...")
    pygame.init()
    print("pygame initialized")
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    print("Display mode set")
    pygame.display.set_caption("Asteroid Game")
    print("Game has started!")
    clock = pygame.time.Clock()
    print(f"FPS: {clock.get_fps()}")
    running = True

    # Create a Game instance
    game = Game(screen_width, screen_height)
    print("Game instance created")

    while running:
        print("Game loop running")
        dt = clock.tick(60) / 1000  # Calculate the delta time

        events = pygame.event.get()  # Collect all events at once
        for event in events:
            print(f"Event type: {event.type}")
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Process menu, playing, and pause states based on key presses
                if game.state == GameState.MENU:
                    if event.key == pygame.K_UP:
                        game.main_menu_selected -= 1
                        if game.main_menu_selected < 0:
                            game.main_menu_selected = len(game.main_menu_options) - 1
                    elif event.key == pygame.K_DOWN:
                        game.main_menu_selected += 1
                        if game.main_menu_selected >= len(game.main_menu_options):
                            game.main_menu_selected = 0
                    elif event.key == pygame.K_RETURN:
                        selected = game.main_menu_options[game.main_menu_selected]
                        if selected == "START":
                            game.state = GameState.PLAYING
                        elif selected == "SELECT DIFFICULTY":
                            pass
                        elif selected == "QUIT":
                            running = False
                        elif selected == "START FROM LEVEL 1":
                            game.state = GameState.PLAYING
                            game.current_level_index = 0
                            game.setup_level(game.levels[0])
                        elif selected == "START FROM LEVEL 2":
                            game.state = GameState.PLAYING
                            game.current_level_index = 1
                            game.setup_level(game.levels[1])
                        elif selected == "START FROM LEVEL 3":
                            game.state = GameState.PLAYING
                            game.current_level_index = 2
                            game.setup_level(game.levels[2])

                # Handle the PAUSED state (ESC to open menu)
                elif game.state == GameState.PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        game.state = GameState.PAUSED

                elif game.state == GameState.PAUSED:
                    if event.key == pygame.K_UP:
                        game.pause_menu_selected -= 1
                        if game.pause_menu_selected < 0:
                            game.pause_menu_selected = len(game.pause_menu_options) - 1
                    elif event.key == pygame.K_DOWN:
                        game.pause_menu_selected += 1
                        if game.pause_menu_selected >= len(game.pause_menu_options):
                            game.pause_menu_selected = 0
                    elif event.key == pygame.K_RETURN:
                        selected = game.pause_menu_options[game.pause_menu_selected]
                        if selected == "RESUME":
                            game.state = GameState.PLAYING
                        elif selected == "MAIN MENU":
                            game.state = GameState.MENU
                        elif selected == "QUIT":
                            game.state = GameState.QUIT_CONFIRM

        game.update(dt, events, screen)  # Pass events to update method

        screen.fill((0, 0, 0))
        game.draw(screen)
        pygame.display.flip()
        pygame.display.update()

    print(f"Game state: {game.state}")  # Check the current state of the game
    print("Pygame quit successfully")

if __name__ == "__main__":
    main()
    pygame.quit()
