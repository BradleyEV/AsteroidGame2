import random
from obstacles import Asteroid, Alien

LEVELS = [
    {"asteroid_count": 12, "asteroid_speed": 5, "alien_count": 5, "alien_speed": 6},
    {"asteroid_count": 15, "asteroid_speed": 7, "alien_count": 7, "alien_speed": 8},
    {"asteroid_count": 20, "asteroid_speed": 10, "alien_count": 10, "alien_speed": 10},
    {"asteroid_count": 25, "asteroid_speed": 15.5, "alien_count": 15, "alien_speed": 12},
    {"asteroid_count": 30, "asteroid_speed": 20.5,"alien_count": 20, "alien_speed": 18}
]

"""def setup_level(self, level_data):
    self.asteroids.clear()
    self.aliens.clear()
    asteroid_count = level_data["asteroid_count"]
    asteroid_speed = level_data["asteroid_speed"]
    alien_count = level_data.get("alien_count", 0) # Default 0 if not set
    alien_speed = level_data.get("alien_speed", 3)

    # Spawn Asteroids
    for _ in range(asteroid_count):
        # Randomize position and speed for asteroids
        width = random.randint(30, 50)
        height = random.randint(30, 50)
        x = random.randint(0, self.screen_width - width)
        y = random.randint(-200, 0)
        speed_x = 0
        speed_y = asteroid_speed * 10

        new_asteroid = Asteroid(x, y, width, height, speed_x, speed_y)
        self.asteroids.append(new_asteroid)

    # Spawn Aliens
    for _ in range(alien_count):
        x = random.randint(0, self.screen_width - 50)
        y = random.randint(0, 100)
        new_alien = Alien(x, y, speed=alien_speed)
        self.aliens.append(new_alien)

    print(f"Level {self.current_level_index + 1}: {asteroid_count} asteroids at speed {asteroid_speed}")"""

def level_complete(self):
    """Move to the next level or finish the game."""
    self.score += 100  # Bonus points for completing the level
    self.current_level_index += 1
    if self.current_level_index < len(self.levels):
        self.setup_level(self.levels[self.current_level_index])  # Setup the next level
    else:
        self.game_over = True  # End game when all levels are complete