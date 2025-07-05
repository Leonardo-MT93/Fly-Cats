# Archivo de configuraciones a cargo de León! 

import pygame
from config import *
from utils import  cargar_musica, reproducir_musica, detener_musica, mostrar_modal_puntuaciones, mostrar_modal_creditos, reproducir_musica_si_necesario
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

    y_start = 350
    rectangulos = []
    for i in range(len(opciones)):
        opcion = opciones[i]
        
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
        #Rectangulos creados a partir de cada opción del menú
        rect = pygame.Rect(x - 50 , y - 10, texto.get_width() + 100, texto.get_height() + 20)
        rectangulos.append(rect)

        # DIibujo test de cada rectangulo
        if i == opcion_seleccionada:
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)  # Amarillo para seleccionado
        else:
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)     # Rojo para no seleccionado
        
        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, color_amarillo)
            screen.blit(indicador, (x - 50, y))
        
        screen.blit(texto, (x, y))
    
    # Instrucciones para que el usuario sepa cómo navegar en el juego..
    instruccion = font_small.render("Usa UP/DOWN para navegar, ENTER para seleccionar", 
                                   True, color_verde)
    instr_x = SCREEN_WIDTH // 2 - instruccion.get_width() // 2
    screen.blit(instruccion, (instr_x, SCREEN_HEIGHT - 30))

    return rectangulos #Aca devolvemos los rectangulos para poder  usarlos en el evento del mouse

def pantalla_menu_principal(screen, clock, imagen_fondo):
    """Pantalla del menú principal"""
    opciones = ["JUGAR", "RANKING", "CREDITOS", "SALIR"]
    opcion_seleccionada = 0
    contador_parpadeo = 0
    
    reproducir_musica_si_necesario(RUTA_MUSICA_MENU, VOLUMEN_MENU)
    # cargar_musica("assets/sounds/music/menu_music.ogg")
    # reproducir_musica(volumen=0.1)
    
    juego_activo = 1
    while juego_activo:
        pos_mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                detener_musica()
                return "SALIR"
            
            # Variable para controlar la opcion ejecutada
            opcion_ejecutada = False
           
            # Teclado
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP:
                    opcion_seleccionada = opcion_seleccionada - 1
                    if opcion_seleccionada < 0:
                        opcion_seleccionada = len(opciones) - 1 
                elif event.key == pygame.K_DOWN:
                    opcion_seleccionada = opcion_seleccionada + 1
                    if opcion_seleccionada >= len(opciones):
                        opcion_seleccionada = 0 
                
                elif event.key == pygame.K_RETURN:
                    opcion_ejecutada = True
            
            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    rectangulos = dibujar_menu_principal(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo)
                    
                    # Verificamos que el mouse colisione con los rectangulos
                    for i in range(len(rectangulos)):
                        rect = rectangulos[i]
                        if rect.collidepoint(event.pos):
                            opcion_seleccionada = i  # Cambiar a la opción clickeada
                            opcion_ejecutada = True  
                            break
            
            if opcion_ejecutada:
                if opciones[opcion_seleccionada] == "JUGAR" or opciones[opcion_seleccionada] == "SALIR":
                    detener_musica()
                return opciones[opcion_seleccionada]

        
        contador_parpadeo += 1
        
        # Efecto hover para el mouse
        rectangulos = dibujar_menu_principal(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo)
        if rectangulos:
            for i in range(len(rectangulos)):
                rect = rectangulos[i]
                if rect.collidepoint(pos_mouse):
                    opcion_seleccionada = i
                    break
       
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
    for i in range(len(mensajes)):
        texto = font_small.render(mensajes[i], True, color_gris)
        x = SCREEN_WIDTH // 2 - texto.get_width() // 2
        screen.blit(texto, (x, 250 + i * 30))
    
    # Opciones del menú
    y_start = 380
    rectangulos = []
    for i in range(len(opciones)):
        opcion = opciones[i]
        # Parpadeo
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
        #creacion de los rectangulos
        rect = pygame.Rect(x - 50 , y - 10, texto.get_width() + 100, texto.get_height() + 20)
        rectangulos.append(rect)
        # DIibujo test de cada rectangulo
        if i == opcion_seleccionada:
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)  # Amarillo para seleccionado
        else:
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)     # Rojo para no seleccionado
        

        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, color_amarillo)
            screen.blit(indicador, (x - 40, y))
        
        screen.blit(texto, (x, y))
    
    # Instrucciones PARA navegar en el menu 
    instruccion = font_small.render("Usa UP/DOWN para navegar, ENTER para seleccionar", 
                                   True, color_verde)
    instr_x = SCREEN_WIDTH // 2 - instruccion.get_width() // 2
    screen.blit(instruccion, (instr_x, SCREEN_HEIGHT - 30))

    return rectangulos

def pantalla_game_over(screen, clock, imagen_fondo_final, puntuacion=0):
    """Pantalla de fin del juego"""
    opciones = ["REINTENTAR", "RANKING", "SALIR"]
    opcion_seleccionada = 0
    contador_parpadeo = 0
    
    # Reproducir música de game over
    reproducir_musica_si_necesario(RUTA_MUSICA_GAME_OVER, VOLUMEN_GAME_OVER)
    # cargar_musica("assets/sounds/music/game_over_music.ogg")
    # reproducir_musica(volumen=0.1)
    
    juego_activo = 1
    while juego_activo:
        pos_mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                detener_musica()
                return "SALIR"
            
            opcion_ejecutada = False
            
            # Teclado
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP:
                    opcion_seleccionada = opcion_seleccionada - 1
                    if opcion_seleccionada < 0:
                        opcion_seleccionada = len(opciones) - 1
                elif event.key == pygame.K_DOWN:
                    opcion_seleccionada = opcion_seleccionada + 1
                    if opcion_seleccionada >= len(opciones):
                        opcion_seleccionada = 0
                
                elif event.key == pygame.K_RETURN:
                    opcion_ejecutada = True
            
            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    rectangulos = dibujar_game_over(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo_final, puntuacion)
                    
                    # Verificamos que el mouse colisione con los rectangulos
                    for i in range(len(rectangulos)):
                        rect = rectangulos[i]
                        if rect.collidepoint(event.pos):
                            opcion_seleccionada = i  # Cambiar a la opción clickeada
                            opcion_ejecutada = True  
                            break
            
            if opcion_ejecutada:
                if opciones[opcion_seleccionada] == "REINTENTAR" or opciones[opcion_seleccionada] == "SALIR":
                    detener_musica()
                return opciones[opcion_seleccionada]
        
        contador_parpadeo += 1
        
        # Efecto hover para el mouse
        rectangulos = dibujar_game_over(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo_final, puntuacion)
        if rectangulos:
            for i in range(len(rectangulos)):
                rect = rectangulos[i]
                if rect.collidepoint(pos_mouse):
                    opcion_seleccionada = i
                    break
        
        pygame.display.flip()
        clock.tick(FPS)
 
def pantalla_juego(screen, clock, imagen_pantalla_juego):
    """Pantalla de juego - completamente para completar por Vish/Agos"""
    font_small = pygame.font.Font(None, 32)
    cargar_musica("assets/sounds/music/game_music.ogg")
    reproducir_musica(volumen=0.1)
    # 
    #carga la imagen de la pantalla de juego con imagen_pantalla_juego

    imagen_jugador, rect_jugador, velocidad_jugador = crear_jugador(screen.get_width(), screen.get_height())
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
                    detener_musica()
                    return "MENU"
                elif event.key == pygame.K_5:
                    detener_musica()
                    return "GAME_OVER"

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        mover_jugador(rect_jugador, keys, screen.get_width(), screen.get_height(), velocidad_jugador)


        # Disparo de balas
        if keys[pygame.K_SPACE]:
            if not disparar:
                imagen_bala, rect_bala, velocidad_bala = crear_bala(rect_jugador.centerx, rect_jugador.top)
                balas.append((imagen_bala, rect_bala, velocidad_bala))
                disparar = True
        else:
            disparar = False

        # Movimiento y limpieza de balas
        for bala in balas[:]:
            imagen, rect, velocidad = bala
            mover_bala(rect, velocidad)
            if bala_fuera_de_pantalla(rect):
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
        dibujar_jugador(screen, imagen_jugador, rect_jugador)
        for bala in balas:
            imagen, rect, _ = bala
            dibujar_bala(screen, imagen, rect)

        # Instrucciones en pantalla
        instrucciones = ["ESC - Volver al menú", "5 - Simular fin del juego"]
        for i, instruccion in enumerate(instrucciones):
            texto = font_small.render(instruccion, True, COLOR_VERDE)
            screen.blit(texto, (20, 20 + i * 35))

        pygame.display.flip()
        clock.tick(FPS)


def procesar_puntuacion():
    "procesa el puntaje obtenido"

def manejar_estado_menu_principal(screen, clock, imagenes):
    """Maneja el estado del menú principal"""
    resultado = pantalla_menu_principal(screen, clock, imagenes['fondos']['menu'])

    match resultado:
            case "JUGAR":
                    return ESTADO_JUEGO, 0
            case "RANKING":
                resultado_ranking = mostrar_modal_puntuaciones(screen, clock, imagenes['fondos']['menu'])
                if resultado_ranking == "SALIR":
                    return None, 0
                return ESTADO_MENU, 0
            case "CREDITOS":
                resultado_creditos = mostrar_modal_creditos(screen, clock, imagenes['fondos']['menu'])
                if resultado_creditos == "SALIR":
                    return None, 0
                return ESTADO_MENU, 0
            case "SALIR":
                    return None, 0
            case _:
                    return ESTADO_MENU, 0
        

def manejar_estado_juego(screen, clock, imagenes):
    resultado = pantalla_juego(screen, clock, imagenes['fondos']['juego'])

    match resultado:
        case "MENU":
            return ESTADO_MENU, 0
        case "GAME_OVER":
            #falta implementar logica de puntaje obtenido
            # puntuacion, es_record = procesar_puntuacion() 
            # return ESTADO_GAME_OVER, puntuacion
            return ESTADO_GAME_OVER, 0
        case "SALIR":
            return None, 0
        case _:
            return ESTADO_JUEGO, 0

def manejar_estado_gameover(screen, clock, imagenes, puntuacion):
    """Maneja el estado de game over"""
    resultado = pantalla_game_over(screen, clock, imagenes['fondos']['game_over'], puntuacion)

    match resultado:
        case "REINTENTAR":
            return ESTADO_JUEGO, 0
        case "RANKING":
            resultado_ranking = mostrar_modal_puntuaciones(screen, clock, imagenes['fondos']['game_over'])
            if resultado_ranking == "SALIR":
                return None, 0
            return ESTADO_GAME_OVER, puntuacion
        case "MENU":
            return ESTADO_MENU, 0
        case "SALIR":
            return None, 0
        
