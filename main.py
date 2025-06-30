import pygame
import sys
import random
from config import *
from utils import cargar_imagen_fondo, es_nuevo_record, agregar_puntuacion_csv, obtener_nombre_jugador
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
    
    juego_activo = 1
    while juego_activo:
        if estado_actual == "MENU":
            resultado = mostrar_menu_principal(screen, clock, imagen_fondo)
            
            if resultado == "JUGAR":
                estado_actual = "JUEGO"
                puntuacion_actual = 0
            elif resultado == "SALIR":
                juego_activo = 0
                
        elif estado_actual == "JUEGO":
            resultado = pantalla_juego(screen, clock)
            
            if resultado == "MENU":
                estado_actual = "MENU"
            elif resultado == "GAME_OVER":
                puntuacion_actual = random.randint(1000, 9999)
                
                # VERIFICAR SI ES NUEVO RÉCORD Y AGREGAR AL CSV
                if es_nuevo_record(puntuacion_actual):
                    # Obtener nombre del jugador
                    nombre_jugador = obtener_nombre_jugador(screen, clock, imagen_fondo)
                    # Agregar al CSV
                    agregar_puntuacion_csv(nombre_jugador, puntuacion_actual)
                    print(f"¡NUEVO RÉCORD! {nombre_jugador}: {puntuacion_actual}")
                else:
                    # También agregar puntuaciones normales al historial
                    agregar_puntuacion_csv("JUGADOR", puntuacion_actual)
                    print(f"Puntuación agregada: {puntuacion_actual}")
                
                estado_actual = "GAME_OVER"
            elif resultado == "SALIR":
                juego_activo = 0

                
        elif estado_actual == "GAME_OVER":
            resultado = pantalla_game_over(screen, clock, imagen_fondo_final, puntuacion_actual)
            
            if resultado == "JUGAR":
                estado_actual = "JUEGO"
                puntuacion_actual = 0
            elif resultado == "MENU":
                estado_actual = "MENU"
            elif resultado == "SALIR":
                juego_activo = 0
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()