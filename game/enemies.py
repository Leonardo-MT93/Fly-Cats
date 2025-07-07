# Archivo de configuraciones a cargo de Vish! 

# Enemigos: Perro robot, perro robot 2 (mas dureza)

import pygame
import config
import random

imagen_enemigo1 = pygame.image.load("assets/images/enemies/Perro_robot_cayendo.png")
imagen_enemigo1_escalada = pygame.transform.scale(imagen_enemigo1, (85,85))
imagen_enemigo2 = pygame.image.load("assets/images/enemies/Enemigo2.png")
imagen_enemigo2_escalada = pygame.transform.scale(imagen_enemigo2, (105, 105))

def crear_enemigo() -> dict :
    """
    Crea enemigos de forma aleatoria y en distintos tiempos, y los posiciona siempre
    dentro de la pantalla
    """
    enemigo_creado = {
        "x": random.randint(0, config.SCREEN_WIDTH - 85),  # 85 es el ancho de la imagen
        "y": random.randint(-500, -50),  # Para que aparezcan en momentos distintos
        "velocidad_y": random.randint(3, 5),
        "activo": False,
        "tiempo_espera": random.randint(60, 3600)
    }
    return enemigo_creado

def crear_enemigo2() -> dict :
    """
    Crea los segundos enemigos, tiempo y velocidad distinta
    """
    enemigo_creado2 = {
        "x": random.randint(0, config.SCREEN_WIDTH - 105),  # 105 es el ancho de la imagen
        "y": random.randint(-500, -50),  # Para que aparezcan en momentos distintos
        "velocidad_y": 3,
        "activo": False,
        "tiempo_espera": random.randint(60, 3600)
    }
    return enemigo_creado2          
