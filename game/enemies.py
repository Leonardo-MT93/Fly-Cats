# Archivo de configuraciones a cargo de Vish! 

# Enemigos: Perro robot

import pygame
import config
import random

alto = config.SCREEN_HEIGHT
imagen_enemigo1 = pygame.image.load("assets/images/enemies/Perro_robot_cayendo.png")
imagen_enemigo1_escalada = pygame.transform.scale(imagen_enemigo1, (85, 85))
enemigo_rect = imagen_enemigo1_escalada.get_rect()


def crear_enemigo() -> dict :
    """
    Crea enemigos de forma aleatoria y en distintos tiempos, y los posiciona siempre
    dentro de la pantalla
    """
    enemigo_creado = {
        "x": random.randint(0, config.SCREEN_WIDTH - 85),  # 85 es el ancho de la imagen
        "y": random.randint(-500, -50),  # Para que aparezcan en momentos distintos
        "velocidad_y": random.randint(3, 6),
        "activo": False,
        "tiempo_espera": random.randint(60, 3600)
    }
    return enemigo_creado

def mover_enemigo(enemigo: dict):
    """
    Mueve al enemigo de acuerdo a su velocidad
    """
    enemigo["y"] += enemigo["velocidad_y"]

def crear_objetos (crear_funcion, cantidad):
    """
    Genera una lista (en este caso la usamos para enemigos y power ups)
    """    
    lista = []
    for i in range(cantidad):
        lista.append(crear_funcion())
    return lista

def caer_objeto(objeto: dict):
    if objeto["tiempo_espera"] > 0:
        objeto["tiempo_espera"] -= 1
    else:
        objeto["activo"] = True

    if objeto["activo"]:
        objeto["y"] += objeto["velocidad_y"]
        if objeto["y"] > config.SCREEN_HEIGHT:
            objeto["activo"] = False