from config import *
from utils import *
from game.game_manager import *

def main():
    screen, clock = iniciar_juego()
    imagenes = cargar_todas_las_imagenes()
    estado_actual = ESTADO_INTRO
    puntuacion_actual = 0
    juego_activo = 1
    
    while juego_activo:
        
        if estado_actual == ESTADO_INTRO:
            estado_actual, puntuacion_actual = manejar_estado_intro(screen, clock, imagenes)

        elif estado_actual == ESTADO_MENU:
            estado_actual, puntuacion_actual = manejar_estado_menu_principal(screen, clock, imagenes)
            
        elif estado_actual == ESTADO_JUEGO:
            estado_actual, puntuacion_actual = manejar_estado_juego(screen, clock, imagenes)
        elif estado_actual == ESTADO_NUEVO_RECORD:
            estado_actual, puntuacion_actual = manejar_estado_nuevo_record(screen, clock, imagenes, puntuacion_actual)
        elif estado_actual == ESTADO_GAME_OVER:
            estado_actual, puntuacion_actual = manejar_estado_gameover(screen, clock, imagenes, puntuacion_actual)
        
        # Si estado_actual es None, salir del juego
        if estado_actual is None:
            juego_activo = 0
    
    finalizar_juego()

main()