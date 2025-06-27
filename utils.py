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

# Musica del juego

def cargar_musica(ruta_musica):
    """Carga una canción"""
    pygame.mixer.music.load(ruta_musica)

def reproducir_musica(volumen=0.7, loops=-1):
    """Reproduce la música cargada"""
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(loops)  # loops=-1 significa repetir infinitamente

def detener_musica():
    """Detiene la música actual"""
    pygame.mixer.music.stop()
