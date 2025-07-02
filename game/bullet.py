<<<<<<< HEAD
# Archivo de configuraciones a cargo de Agos! 
import pygame

=======
# Archivo de configuraciones a cargo de Agos! import pygame
import pygame
>>>>>>> fa8f46c76360a7c8312c81b6b13e54f97f3fd5e4
def crear_bala(x, y):
    bala = {}
    bala['image'] = pygame.image.load("assets/images/bola-estambre.png").convert_alpha()
    bala['image'] = pygame.transform.scale(bala['image'], (25, 25))
    bala['rect'] = bala['image'].get_rect(center=(x, y))
    bala['speed'] = -8
    return bala


def mover_bala(bala):
    bala['rect'].y += bala['speed']

def dibujar_bala(screen, bala):
    screen.blit(bala['image'], bala['rect'])

def bala_fuera_de_pantalla(bala):
    return bala['rect'].bottom < 0