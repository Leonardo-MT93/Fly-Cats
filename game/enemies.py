# Archivo de configuraciones a cargo de Vish! 

# Enemigos: Perro robot

import pygame
import config
import random

alto = config.SCREEN_HEIGHT
imagen_enemigo1 = pygame.image.load("assets/images/enemies/Perro_robot_cayendo.png")
imagen_enemigo1_escalada = pygame.transform.scale(imagen_enemigo1, (85, 85))
enemigo_rect = imagen_enemigo1_escalada.get_rect()


def crear_enemigo():
    """
    Crea enemigos de forma aleatoria, y los posiciona siempre
    dentro de la pantalla
    """
    enemigo_creado = {
        "x": random.randint(0, config.SCREEN_WIDTH - 85),  # 85 es el ancho de la imagen
        "y": random.randint(-150, -50),  # Para que aparezcan en momentos distintos
        "velocidad_y": random.randint(3, 6)
    }
    return enemigo_creado

def mover_enemigo(enemigo: dict):
    """
    Mueve al enemigo de acuerdo a su velocidad
    """
    enemigo["y"] += enemigo["velocidad_y"]
