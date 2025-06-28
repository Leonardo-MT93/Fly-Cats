import pygame
import sys
import random
from config import *
from utils import cargar_imagen_fondo
from game.game_manager import mostrar_menu_principal, pantalla_juego, pantalla_game_over

def main():
    """Función principal que maneja todas las pantallas"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fly Cats")
    clock = pygame.time.Clock()
    icono = pygame.image.load(RUTA_ICONO_JUEGO)
    pygame.display.set_icon(icono)
    
    #Checklist: Cargar imagen de fondo del juego - falta modificar
    imagen_fondo = cargar_imagen_fondo(RUTA_IMAGEN_FONDO_MENU_PRINCIPAL)
    imagen_fondo_final = cargar_imagen_fondo(RUTA_IMAGEN_FIN_DEL_JUEGO)
    
    estado_actual = "MENU"
    puntuacion_actual = 0
    
    while True:
        if estado_actual == "MENU":
            resultado = mostrar_menu_principal(screen, clock, imagen_fondo)
            
            if resultado == "JUGAR":
                estado_actual = "JUEGO"
                puntuacion_actual = 0
            elif resultado == "PUNTUACIONES":
                print("Mostrar puntuaciones...")  #Checklist: Falta terminar..
            elif resultado == "OPCIONES":
                print("Mostrar opciones...")  #Checklist: Falta terminar..
            elif resultado == "SALIR":
                break
                
        elif estado_actual == "JUEGO":
            resultado = pantalla_juego(screen, clock)
            
            if resultado == "MENU":
                estado_actual = "MENU"
            elif resultado == "GAME_OVER":
                #Checklist: Puntuación implementar.. 
                puntuacion_actual = random.randint(1000, 9999)
                estado_actual = "GAME_OVER"
            elif resultado == "SALIR":
                break
                
        elif estado_actual == "GAME_OVER":
            resultado = pantalla_game_over(screen, clock, imagen_fondo_final, puntuacion_actual)
            
            if resultado == "JUGAR":
                estado_actual = "JUEGO"
                puntuacion_actual = 0
            elif resultado == "MENU":
                estado_actual = "MENU"
            elif resultado == "SALIR":
                break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()