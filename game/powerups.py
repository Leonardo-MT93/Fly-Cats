# Archivo de configuraciones a cargo de Vish! 

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, RUTA_POWER_UP_ATUN, RUTA_POWER_UP_MILK
import random

atun = pygame.image.load(RUTA_POWER_UP_ATUN)
atun_escalada = pygame.transform.scale(atun, (85, 85))

milk = pygame.image.load(RUTA_POWER_UP_MILK)
milk_escalada = pygame.transform.scale(milk, (85, 85))


def crear_atun():
    """
    Crea un power up "atun"
    """
    atun_creado = {
        "x": random.randint(0, SCREEN_WIDTH - 85),  # 85 ancho de la imagen
        "y": random.randint(-150, -50),  # Para que aparezcan en momentos distintos
        "velocidad_y": random.randint(2, 4),
        "activo": False,
        "tiempo_espera": random.randint(60, 3600)
    }
    return atun_creado


def caer_atun(atun: dict):
    """
    Caida del atun
    """
    atun["y"] += atun["velocidad_y"]

def crear_milk():
    """
    Crea un power up "leche"
    """
    milk_creada = {
        "x": random.randint(0, SCREEN_WIDTH - 85),
        "y": random.randint(-150, -50),
        "velocidad_y": random.randint(2, 4),
        "activo": False,
        "tiempo_espera": random.randint(60, 3600)
    }
    return milk_creada

def caer_milk(milk: dict):
    """
    Caida de la botella de leche
    """
    milk["y"] += milk["velocidad_y"]
    