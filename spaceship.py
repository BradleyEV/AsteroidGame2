import pygame
import os

class Spaceship:
    def __init__ (self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = 0
        self.dy = 0

        self.health = 3

        # For drawing: you might eventually load an image

        image_path = os.path.join("Assets", "Spaceship.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80)) # Scale the image to a desired size (64x64)

        # For collisions, keep a rect updated
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Shrink the collision rect by 20% in each dimension, or similar
        self.rect = self.rect.inflate(-10, -10)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Left/Right
        if keys[pygame.K_LEFT]:
            self.dx = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.dx = self.speed
        else:
            self.dx = 0

        # Up/Down
        if keys[pygame.K_UP]:
            self.dy = -self.speed
        elif keys[pygame.K_DOWN]:
            self.dy = self.speed
        else:
            self.dy = 0

        # Apply delta time
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Keep the rect in sync with the new x, y
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        # For now, draw a simple rectangle or a circle as a placeholder
        screen.blit(self.image, (self.x, self.y))
        # Or if you have an image:
        # screen.blit(self.image, (self.x, self.y))
