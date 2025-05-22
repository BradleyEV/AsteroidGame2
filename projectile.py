import pygame

class Projectile:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed  # Speed is positive but will be used to move the projectile upwards
        self.width = 5
        self.height = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load('Assets/Projectile2.png').convert_alpha()  # Relative path to the image


    def update(self):
        self.y -= self.speed  # Subtract speed to move upward
        self.rect.y = self.y  # Update the rect to match the position

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))