# Archivo de configuraciones a cargo de Vish! 

# Enemigos: Perro robot

import pygame
import config
import random

alto = config.SCREEN_HEIGHT
imagen_enemigo1 = pygame.image.load("assets/images/enemies/Perro_robot_cayendo.png")
imagen_enemigo1_escalada = pygame.transform.scale(imagen_enemigo1, (85, 85))
imagen_enemigo2 = pygame.image.load("assets/images/enemies/Enemigo2.png")
imagen_enemigo2_escalada = pygame.transform.scale(imagen_enemigo2, (85, 85))
enemigo_rect = imagen_enemigo1_escalada.get_rect()
enemigo_rect2 = imagen_enemigo2_escalada.get_rect()



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

def crear_enemigo2() -> dict :
    """
    Crea los segundos enemigos, tiempo y velocidad distinta
    """
    enemigo_creado2 = {
        "x": random.randint(0, config.SCREEN_WIDTH - 85),  # 85 es el ancho de la imagen
        "y": random.randint(-500, -50),  # Para que aparezcan en momentos distintos
        "velocidad_y": 3,
        "activo": False,
        "tiempo_espera": random.randint(60, 3600)
    }
    return enemigo_creado2


def crear_objetos (crear_funcion, cantidad:int) -> list :
    """
    Genera una lista (en este caso la usamos para enemigos y power ups)
    """    
    lista = []
    for i in range(cantidad):
        lista.append(crear_funcion())
    return lista

def caer_objeto(objeto: dict):
    """
    Se le pasa un diccionario, lo modifica y actualiza, de acuerdo al estado, tiempo y velocidad de aparicion
    """
    if objeto["tiempo_espera"] > 0:
        objeto["tiempo_espera"] -= 1
    else:
        objeto["activo"] = True

    if objeto["activo"]:
        objeto["y"] += objeto["velocidad_y"]
        
        # Reiniciar para que vuelva a caer
        if objeto["y"] > config.SCREEN_HEIGHT:
            objeto["x"] = random.randint(0, config.SCREEN_WIDTH - 85)
            objeto["y"] = random.randint(-500, -50)
            objeto["velocidad_y"] = random.randint(3, 6)  # o lo que corresponda
            objeto["tiempo_espera"] = random.randint(60, 3600)
            objeto["activo"] = False