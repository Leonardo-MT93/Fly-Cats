# Archivo de configuraciones a cargo de León! 
from config import *
import pygame

def cargar_imagen_fondo(ruta_imagen):
    """Carga y escala la imagen de fondo"""
    imagen = pygame.image.load(ruta_imagen)
    imagen_escalada = pygame.transform.scale(imagen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return imagen_escalada

def cargar_imagen_fondo_final(ruta_imagen):
    """Carga y escala la imagen de fondo del final del juego"""
    imagen = pygame.image.load(ruta_imagen)
    imagen_escalada = pygame.transform.scale(imagen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return imagen_escalada