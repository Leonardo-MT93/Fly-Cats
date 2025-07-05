# Archivo de configuraciones a cargo de León! 

import pygame
from config import *
from utils import  cargar_musica, reproducir_musica, detener_musica, mostrar_modal_puntuaciones
from game.player import crear_jugador, mover_jugador, dibujar_jugador
from game.bullet import crear_bala, mover_bala, dibujar_bala, bala_fuera_de_pantalla
from game.enemies import crear_enemigo, imagen_enemigo1_escalada, crear_objetos, caer_objeto
from game.powerups import crear_atun, crear_milk, caer_atun, caer_milk, atun_escalada, milk_escalada

def dibujar_menu_principal(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo):
    """Dibuja el menú principal del juego"""
    font_botones = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    color_verde = COLOR_VERDE
    color_blanco = COLOR_BLANCO
    color_amarillo = COLOR_AMARILLO
    
    # Dibujar fondo
    screen.blit(imagen_fondo, (0, 0))
    
    # Opciones del menú
    y_start = 350
    for i, opcion in enumerate(opciones):
        if i == opcion_seleccionada:
            if contador_parpadeo % 30 < 15:
                color = color_amarillo
            else:
                color = color_blanco
        else:
            color = color_blanco
        
        texto = font_botones.render(opcion, True, color)
        x = SCREEN_WIDTH // 2 - texto.get_width() // 2
        y = y_start + i * 60
        
        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, color_amarillo)
            screen.blit(indicador, (x - 50, y))
        
        screen.blit(texto, (x, y))
    
    # Instrucciones para que el usuario sepa cómo navegar en el juego..
    instruccion = font_small.render("Usa UP/DOWN para navegar, ENTER para seleccionar", 
                                   True, color_verde)
    instr_x = SCREEN_WIDTH // 2 - instruccion.get_width() // 2
    screen.blit(instruccion, (instr_x, SCREEN_HEIGHT - 30)) #Posicion de la instruccion en el eje Y

def mostrar_menu_principal(screen, clock, imagen_fondo):
    """Pantalla del menú principal"""
    opciones = ["JUGAR", "PUNTUACIONES", "SALIR"]
    opcion_seleccionada = 0
    contador_parpadeo = 0

    # Reproducir música del menú
    cargar_musica("assets/sounds/music/menu_music.ogg")
    reproducir_musica(volumen=0.1)
    juego_activo = 1

    while juego_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                detener_musica()
                return "SALIR"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    #Aca se agrega el modal de puntuaciones
                    if opciones[opcion_seleccionada] == "PUNTUACIONES":
                        # Mostrar modal sin detener música de pantalla principl
                        resultado = mostrar_modal_puntuaciones(screen, clock, imagen_fondo)
                        if resultado == "SALIR":
                            detener_musica()
                            return "SALIR"
                    else:
                        detener_musica()  # Detiene la música al salir del menú
                        return opciones[opcion_seleccionada]
        
        contador_parpadeo += 1
        dibujar_menu_principal(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo)
        
        pygame.display.flip()
        clock.tick(FPS)


def dibujar_game_over(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo_final, puntuacion=0):
    """Dibuja la pantalla de game over"""
    font_subtitulo = pygame.font.Font(None, 48)
    font_botones = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)
    
    color_blanco = COLOR_BLANCO
    color_amarillo = COLOR_AMARILLO
    color_verde = COLOR_VERDE
    color_gris = COLOR_GRIS
    
    # Dibuja fondo (igual que el menú principal)
    screen.blit(imagen_fondo_final, (0, 0))
    
    #Checklist: Puntuación final ficticio - falta implementar
    puntuacion_texto = font_subtitulo.render(f"Puntuación Final: {puntuacion}", True, color_amarillo)
    punt_x = SCREEN_WIDTH // 2 - puntuacion_texto.get_width() // 2
    screen.blit(puntuacion_texto, (punt_x, 180))
    
    # Mensaje motivacional de fin del juego
    mensajes = [
        "¡Los invasores han ganado esta vez! " " ¡Pero la Tierra aún tiene esperanza!"
        ,
        "¿Intentarás defender el planeta otra vez?"
    ]
    
    for i, mensaje in enumerate(mensajes):
        texto = font_small.render(mensaje, True, color_gris)
        x = SCREEN_WIDTH // 2 - texto.get_width() // 2
        screen.blit(texto, (x, 250 + i * 30))
    
    # Opciones del menú
    y_start = 380
    for i, opcion in enumerate(opciones):
        if i == opcion_seleccionada:
            if contador_parpadeo % 30 < 15:
                color = color_amarillo
            else:
                color = color_blanco
        else:
            color = color_blanco
        
        texto = font_botones.render(opcion, True, color)
        x = SCREEN_WIDTH // 2 - texto.get_width() // 2
        y = y_start + i * 50
        
        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, color_amarillo)
            screen.blit(indicador, (x - 40, y))
        
        screen.blit(texto, (x, y))
    
    # Instrucciones PARA navegar en el menu 
    instruccion = font_small.render("Usa UP/DOWN para navegar, ENTER para seleccionar", 
                                   True, color_verde)
    instr_x = SCREEN_WIDTH // 2 - instruccion.get_width() // 2
    screen.blit(instruccion, (instr_x, SCREEN_HEIGHT - 30))

def pantalla_game_over(screen, clock, imagen_fondo_final, puntuacion=0):
    """Pantalla de fin del juego"""
    opciones = ["REINTENTAR", "PUNTUACIONES", "SALIR"]
    opcion_seleccionada = 0
    contador_parpadeo = 0

    # Reproducir música de game over
    cargar_musica("assets/sounds/music/game_over_music.ogg")
    reproducir_musica(volumen=0.1)

    juego_activo = 1
    while juego_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                detener_musica()
                return "SALIR"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    #AAca agregamos el modal que lee los puntajes del csv
                    if opciones[opcion_seleccionada] == "PUNTUACIONES":
                        # Muestra el modal sin detener música de la pantalla gameover
                        resultado = mostrar_modal_puntuaciones(screen, clock, imagen_fondo_final)
                        if resultado == "SALIR":
                            detener_musica()
                            return "SALIR"
                        
                    else:
                        detener_musica()  # Detener música al salir del menu findejuego
                        if opciones[opcion_seleccionada] == "REINTENTAR":
                            return "JUGAR"
                        elif opciones[opcion_seleccionada] == "SALIR":
                            return "SALIR"
        
        contador_parpadeo += 1
        dibujar_game_over(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo_final, puntuacion)
        
        pygame.display.flip()
        clock.tick(FPS)
 
def pantalla_juego(screen, clock, imagen_pantalla_juego):
    """Pantalla de juego - completamente negra para completar por Vish/Agos"""
    font_small = pygame.font.Font(None, 32)
    color_verde = COLOR_VERDE
    #carga la imagen de la pantalla de juego con imagen_pantalla_juego

    jugador = crear_jugador(screen.get_width(), screen.get_height())
    balas = []
    disparar = False

    #Creamos listas de los enemigos y power ups que caeran
    enemigos = crear_objetos(crear_enemigo, 35)
    atunes = crear_objetos(crear_atun, 5)
    milks = crear_objetos(crear_milk, 3)

    juego_activo = 1
    while juego_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
                elif event.key == pygame.K_5:
                    return "GAME_OVER"

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        mover_jugador(jugador, keys, screen.get_width(), screen.get_height())

        # Disparo de balas
        if keys[pygame.K_SPACE]:
            if not disparar:
                bala = crear_bala(jugador['rect'].centerx, jugador['rect'].top)
                balas.append(bala)
                disparar = True
        else:
            disparar = False

        # Movimiento y limpieza de balas
        for bala in balas[:]:
            mover_bala(bala)
            if bala_fuera_de_pantalla(bala):
                balas.remove(bala)

        # Fondo de juego
        screen.blit(imagen_pantalla_juego, (0, 0))

        # Hacemos caer los enemigos y power ups, dibuja solo si están activas en pantalla
        for enemigo in enemigos:
            caer_objeto(enemigo)
            if enemigo["activo"]:
                screen.blit(imagen_enemigo1_escalada, (enemigo["x"], enemigo["y"]))

        for atun in atunes:
            caer_objeto(atun)
            if atun["activo"]:
                screen.blit(atun_escalada, (atun["x"], atun["y"]))

        for milk in milks:
            caer_objeto(milk)
            if milk["activo"]:
                screen.blit(milk_escalada, (milk["x"], milk["y"]))            

        # Dibujar jugador y balas
        dibujar_jugador(screen, jugador)
        for bala in balas:
            dibujar_bala(screen, bala)

        # Instrucciones en pantalla
        instrucciones = ["ESC - Volver al menú", "5 - Simular fin del juego"]
        for i, instruccion in enumerate(instrucciones):
            texto = font_small.render(instruccion, True, COLOR_VERDE)
            screen.blit(texto, (20, 20 + i * 35))

        pygame.display.flip()
        clock.tick(FPS)

