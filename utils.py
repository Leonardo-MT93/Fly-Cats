import pygame

def load_image(width, height, color=(255, 0, 255)):
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface