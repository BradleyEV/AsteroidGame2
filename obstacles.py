import pygame
import random
import os

class Asteroid:

    def __init__(self, x, y, width, height, speed_x, speed_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = speed_x
        self.speed_y = speed_y

        # For drawing: you might eventually load an image

        image_path = os.path.join("Assets", "Asteroid.png")
        self.image = pygame.image.load(image_path).convert_alpha()

        # For collisions, keep a rect updated
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt

    def draw(self, screen):
        # For now, draw a simple rectangle or a circle as a placeholder
        screen.blit(self.image, (self.x, self.y))

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @rect.setter
    def rect(self, value):
        self._rect = value

class Alien:
    def __init__(self, x, y, speed=3, direction=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # 1 for right, -1 for left

        image_path = os.path.join("Assets", "Alien.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        # Maybe scale if needed
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, dt, screen_width):
        # Move horizontally
        self.x += self.speed * self.direction * dt
        self.rect.x = self.x

        # Vertical drop
        self.y += self.speed * dt
        self.rect.y = self.y

        # Reverse direction if hitting bounds
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.x = self.rect.x
            self.direction = -1
        elif self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.x
            self.direction = 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
