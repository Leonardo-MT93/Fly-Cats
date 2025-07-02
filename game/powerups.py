# Archivo de configuraciones a cargo de Vish! 

import pygame
import config
import random

alto = config.SCREEN_HEIGHT
atun = pygame.image.load("assets/images/atun.png")
atun_escalada = pygame.transform.scale(atun, (85, 85))
atun_rect = atun_escalada.get_rect()

milk = pygame.image.load("assets/images/Milk power.png")
milk_escalada = pygame.transform.scale(milk, (85, 85))
milk_rect = milk_escalada.get_rect()


def crear_atun():
    """
    Crea un power up "atun"
    """
    atun_creado = {
        "x": random.randint(0, config.SCREEN_WIDTH - 85),  # 85 ancho de la imagen
        "y": random.randint(-150, -50),  # Para que aparezcan en momentos distintos
        "velocidad_y": random.randint(3, 6)
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
        "x": random.randint(0, config.SCREEN_WIDTH - 85),  
        "y": random.randint(-150, -50), 
        "velocidad_y": random.randint(3, 6)
    }
    return milk_creada

def caer_milk(milk: dict):
    """
    Caida de la botella de leche
    """
    milk["y"] += milk["velocidad_y"]
    