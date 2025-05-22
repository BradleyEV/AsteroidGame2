import pygame.font
import pygame
import random
from Utils.collisions import check_rect_collision
from spaceship import Spaceship
from levels import LEVELS
from obstacles import Asteroid, Alien
from projectile import Projectile

class GameState:
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    QUIT_CONFIRM = 3
    GAME_OVER = 4

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.state = GameState.MENU
        # Menu data for the main menu
        self.main_menu_options = ["START", "SELECT DIFFICULTY", "QUIT", "START FROM LEVEL 1", "START FROM LEVEL 2", "START FROM LEVEL 3"]
        self.main_menu_selected = 0

        # Menu data for the pause menu
        self.pause_menu_options = ["RESUME", "MAIN MENU", "QUIT"]
        self.pause_menu_selected = 0

        self.score = 0  # track points or progress

        # Create the spaceship in the center
        self.spaceship = Spaceship(
            x=screen_width // 2,
            y=screen_height // 2,
            speed=200
        )
        self.game_over = False

        # Load levels and start at index 0
        self.levels = LEVELS
        self.current_level_index = 0

        # The asteroid list
        self.asteroids = []

        # The alien list
        self.aliens = []

        # Initialize first level
        self.setup_level(self.levels[self.current_level_index])

        self.projectiles = []

    def setup_level(self, level_data):
        """
        Spawns asteroids based on the dictionary 'level_data',
        e.g., level_data = {"asteroid_count": 5, "asteroid_speed": 2}.
        """
        # Clear out any existing asteroids if we're resetting or going to a new level
        self.asteroids.clear()

        # Pull the asteroid count/speed from the dictionary
        asteroid_count = level_data["asteroid_count"]
        asteroid_speed = level_data["asteroid_speed"]
        print(f"Setting up level with {asteroid_count} asteroids at speed {asteroid_speed}")

        # Spawn multiple asteroids
        for _ in range(asteroid_count):
            #1 ) Random width/height
            width = random.randint(30, 50)
            height = random.randint(30, 50)

            # 2) Random x, y with the new width in mind
            x = random.randint(0, self.screen_width - 40)
            y = random.randint(-200, 0)  # spawn above visible screen

            # 3) Speed logic
            speed_x = 0
            speed_y = asteroid_speed * 10  # multiply to make it faster

            # 4) Create the asteroid using width and height
            new_asteroid = Asteroid(x, y, width, height, speed_x, speed_y)
            self.asteroids.append(new_asteroid)

        # Debug check
        print(f"Number of asteroids spawned: {len(self.asteroids)}")

        self.aliens.clear()  # Clear previous aliens

        # Read alien fields from the level dictionary
        alien_count = level_data.get("alien_count", 0)
        alien_speed = level_data.get("alien_speed", 3)

        for i in range(alien_count):
            # Randomly pick direction
            direction = random.choice([1, -1])

            if direction == 1:
                # Spawn left side
                x = random.randint(0, 50)
            else:
                # Spawn right side
                x = random.randint(self.screen_width - 50, self.screen_width)

            y = random.randint(0, 100)
            new_alien = Alien(x, y, speed=alien_speed, direction=direction)
            self.aliens.append(new_alien)

        print(f"Level {self.current_level_index + 1}: "
              f"{asteroid_count} asteroids, {alien_count} aliens.")

    def level_complete(self):
        """
        Moves to the next level if available; sets game_over if we're out of levels.
        """
        self.score += 100  # Bonus
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.setup_level(self.levels[self.current_level_index])
        else:
            print("No more levels! Game complete.")
            self.game_over = True

    def update(self, dt, events, screen):
        print(f"Current state: {self.state}")

        if self.state == GameState.MENU:
            return

        elif self.state == GameState.PLAYING:
            print("Game is in PLAYING state")
            # Award time-based points
            self.score += 10 * dt

            # -------------------
            # Handle input for firing projectiles
            # -------------------
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        print("Spacebar pressed!")
                        # Fire a new projectile
                        new_projectile = Projectile(self.spaceship.x + 20, self.spaceship.y - 10, 5)
                        self.projectiles.append(new_projectile)
                        print("Projectile fired!")

            # -------------------
            # Update projectiles and check collisions
            # -------------------
            for projectile in self.projectiles[:]:
                projectile.update()

                # Remove projectiles off-screen
                if projectile.y < 0:
                    self.projectiles.remove(projectile)
                    continue

                # Check for collision with asteroids
                for asteroid in self.asteroids[:]:
                    if projectile.rect.colliderect(asteroid.rect):
                        self.asteroids.remove(asteroid)
                        self.projectiles.remove(projectile)
                        self.score += 100
                        # Draw a quick "explosion" at the asteroid center
                        pygame.draw.circle(screen, (255, 0, 0),
                                           (asteroid.rect.centerx, asteroid.rect.centery), 10)
                        break

                # Check collision with aliens
                for alien in self.aliens[:]:
                    if projectile.rect.colliderect(alien.rect):
                        self.aliens.remove(alien)
                        self.projectiles.remove(projectile)
                        self.score += 150  # maybe more points for aliens
                        # If you want an explosion effect, do it here
                        pygame.draw.circle(screen, (255, 0, 0),
                                           (alien.rect.centerx, alien.rect.centery), 10)
                        break

            # -------------------
            # Update the spaceship
            # -------------------
            self.spaceship.update(dt)
            # Spaceship collision rect
            # (Adjust size as needed, or use spaceship.rect if you stored it that way.)
            spaceship_rect = pygame.Rect(self.spaceship.x, self.spaceship.y, 40, 40)

            # -------------------
            # Update asteroids
            # -------------------
            for asteroid in self.asteroids[:]:
                asteroid.update(dt)
                # If off-screen, remove and award partial points
                if asteroid.y > self.screen_height:
                    self.asteroids.remove(asteroid)
                    self.score += 20
                    continue

                # Check collision with spaceship
                if spaceship_rect.colliderect(asteroid.rect):
                    self.asteroids.remove(asteroid)
                    self.spaceship.health -= 1
                    if self.spaceship.health <= 0:
                        self.state = GameState.GAME_OVER
                        self.game_over = True
                        return

            # -------------------
            # Update aliens
            # -------------------
            for alien in self.aliens[:]:
                # If your Alien class has an `update(dt, screen_width)`, call it:
                alien.update(dt, self.screen_width)

                # (Optional) If you want them to drop or do something vertically,
                # your Alien.update() can handle that logic (e.g., self.y += ...)

                # Remove if off-screen vertically (only if they drop)
                # if alien.y > self.screen_height:
                #     self.aliens.remove(alien)
                #     continue

                # Check collision with spaceship
                if spaceship_rect.colliderect(alien.rect):
                    self.aliens.remove(alien)
                    self.spaceship.health -= 1
                    if self.spaceship.health <= 0:
                        self.state = GameState.GAME_OVER
                        self.game_over = True
                        return

            # -------------------
            # Check if level complete
            # -------------------
            if len(self.asteroids) == 0 and len(self.aliens) == 0:
                self.level_complete()

        elif self.state == GameState.GAME_OVER:
            # ...
            pygame.quit()
            print("Game Over")
            return

        elif self.state == GameState.QUIT_CONFIRM:
            # ...
            pass

    def draw(self, screen):
        # If we're in the MENU state
        if self.state == GameState.MENU:
            screen.fill((0, 0, 0))  # Clear background

            # Title
            title_font = pygame.font.SysFont(None, 64)
            title_text = title_font.render("ASTEROID GAME", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
            screen.blit(title_text, title_rect)

            # Options
            menu_font = pygame.font.SysFont(None, 36)
            for i, option in enumerate(self.main_menu_options):
                if i == self.main_menu_selected:
                    color = (255, 255, 0)  # Highlight
                else:
                    color = (255, 255, 255)
                text_surf = menu_font.render(option, True, color)
                text_rect = text_surf.get_rect(center=(self.screen_width // 2, 200 + i * 50))
                screen.blit(text_surf, text_rect)

        # If we're in the PAUSED state
        elif self.state == GameState.PAUSED:
            screen.fill((0, 0, 0))  # Clear screen

            # Draw pause menu
            pause_font = pygame.font.SysFont(None, 64)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 0))
            pause_rect = pause_text.get_rect(center=(self.screen_width // 2, 100))
            screen.blit(pause_text, pause_rect)

            menu_font = pygame.font.SysFont(None, 36)
            for i, option in enumerate(self.pause_menu_options):
                if i == self.pause_menu_selected:
                    color = (255, 255, 0)  # Highlight option
                else:
                    color = (255, 255, 255)
                text_surf = menu_font.render(option, True, color)
                text_rect = text_surf.get_rect(center=(self.screen_width // 2, 200 + i * 50))
                screen.blit(text_surf, text_rect)

        # If we're in the PLAYING state
        elif self.state == GameState.PLAYING:
            # Draw the spaceship
            self.spaceship.draw(screen)

            # Draw all projectiles
            for projectile in self.projectiles:
                projectile.draw(screen)

            # Draw all asteroids
            for asteroid in self.asteroids:
                asteroid.draw(screen)

            # Draw all aliens (NOT update them)
            for alien in self.aliens:
                alien.draw(screen)

            # Simple HUD / Game Over text
            font = pygame.font.SysFont(None, 32)
            if not self.game_over:
                # Show health
                health_text = font.render(f"Health: {self.spaceship.health}", True, (255, 255, 255))
                screen.blit(health_text, (10, 10))
                # Show Score
                score_text = font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
                screen.blit(score_text, (10, 40))  # Just below the health text

        # If we're in the GAME_OVER state
        elif self.state == GameState.GAME_OVER:
            screen.fill((0, 0, 0))  # Clear screen

            # Display GAME OVER message
            over_font = pygame.font.SysFont(None, 64)
            over_text = over_font.render("GAME OVER", True, (255, 0, 0))
            text_rect = over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(over_text, text_rect)

            # Show final score
            font = pygame.font.SysFont(None, 32)
            final_score_text = font.render(f"Final Score: {int(self.score)}", True, (255, 255, 255))
            final_rect = final_score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
            screen.blit(final_score_text, final_rect)

        # If we're in the QUIT_CONFIRM state (confirm quit screen)
        elif self.state == GameState.QUIT_CONFIRM:
            # Draw quit confirmation (Yes/No)
            screen.fill((0, 0, 0))

            quit_font = pygame.font.SysFont(None, 64)
            quit_text = quit_font.render("ARE YOU SURE?", True, (255, 0, 0))
            quit_rect = quit_text.get_rect(center=(self.screen_width // 2, 100))
            screen.blit(quit_text, quit_rect)

            menu_font = pygame.font.SysFont(None, 36)
            for i, option in enumerate(["YES", "NO"]):
                if i == self.pause_menu_selected:
                    color = (255, 255, 0)  # Highlight
                else:
                    color = (255, 255, 255)
                option_surf = menu_font.render(option, True, color)
                option_rect = option_surf.get_rect(center=(self.screen_width // 2, 200 + i * 50))
                screen.blit(option_surf, option_rect)
