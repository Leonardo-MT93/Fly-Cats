# Archivo de configuraciones a cargo de Vish! 

# Enemigos: Perro robot

from game.game_manager import pantalla_juego
import pygame
import config

ancho = config.SCREEN_WIDTH
alto = config.SCREEN_HEIGHT

imagen_enemigo1 = pygame.image.load("assets/images/enemies/Perrorobotvolando.png")
enemigo_rect = imagen_enemigo1.get_rect()

enemigo_x = 100
enemigo_y = 100
velocidad_x = 3

def mover_enemigo(enemigo_x, 
    """
    El primer enemigo se mueve horizontalmente
    """
    enemigo_x = 100
    enemigo_y = 100
    velocidad_x = 3
    enemigo_x += velocidad_x

    # Rebote en los bordes 
    if enemigo_x > ancho - enemigo_rect.width or enemigo_x < 0:
        velocidad_x *= -1

    return enemigo_x