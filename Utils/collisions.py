import math
import pygame

def check_rect_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    rect1 = pygame.Rect(x1, y1, w1, h1)
    rect2 = pygame.Rect(x2, y2, w2, h2)
    return rect1.colliderect(rect2)