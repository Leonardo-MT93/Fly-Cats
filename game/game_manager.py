# Archivo de configuraciones a cargo de León! 

import pygame
from config import *
from utils import  cargar_musica, reproducir_musica, detener_musica, mostrar_modal_puntuaciones, mostrar_modal_creditos, reproducir_musica_si_necesario, es_nuevo_record, agregar_puntuacion_csv, obtener_nombre_jugador
from game.player import crear_jugador, mover_jugador, dibujar_jugador
from game.bullet import crear_bala, mover_bala, dibujar_bala, bala_fuera_de_pantalla
from game.enemies import crear_enemigo, crear_enemigo2, imagen_enemigo1_escalada, imagen_enemigo2_escalada, crear_objetos, caer_objeto, controlar_max_objetos_totales
from game.powerups import crear_atun, crear_milk, atun_escalada, milk_escalada

def dibujar_menu_principal(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo):
    """Dibuja el menú principal del juego"""
    font_botones = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 28)
    
    # Dibujar fondo
    screen.blit(imagen_fondo, (0, 0))

    y_start = 350
    rectangulos = []
    for i in range(len(opciones)):
        opcion = opciones[i]
        
        if i == opcion_seleccionada:
            if contador_parpadeo % 30 < 15:
                color = COLOR_AMARILLO
            else:
                color = COLOR_BLANCO
        else:
            color = COLOR_BLANCO

        
        texto = font_botones.render(opcion, True, color)
        x = SCREEN_WIDTH // 2 - texto.get_width() // 2
        y = y_start + i * 60
        #Rectangulos creados a partir de cada opción del menú
        rect = pygame.Rect(x - 50 , y - 10, texto.get_width() + 100, texto.get_height() + 20)
        rectangulos.append(rect)

        # DIibujo test de cada rectangulo
        # if i == opcion_seleccionada:
        #     pygame.draw.rect(screen, (255, 255, 0), rect, 3)  # Amarillo para seleccionado
        # else:
        #     pygame.draw.rect(screen, (255, 0, 0), rect, 2)     # Rojo para no seleccionado
        
        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, COLOR_AMARILLO)
            screen.blit(indicador, (x - 50, y))
        
        screen.blit(texto, (x, y))
    
    # Instrucciones para que el usuario sepa cómo navegar en el juego..
    instruccion = font_small.render("Usa UP/DOWN para navegar, ENTER para seleccionar", 
                                   True, COLOR_VERDE)
    instr_x = SCREEN_WIDTH // 2 - instruccion.get_width() // 2
    screen.blit(instruccion, (instr_x, SCREEN_HEIGHT - 30))

    return rectangulos #Aca devolvemos los rectangulos para poder  usarlos en el evento del mouse

def pantalla_menu_principal(screen, clock, imagen_fondo):
    """Pantalla del menú principal"""
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
                        opcion_seleccionada = len(OPCIONES_MENU_PRINCIPAL) - 1 
                elif event.key == pygame.K_DOWN:
                    opcion_seleccionada = opcion_seleccionada + 1
                    if opcion_seleccionada >= len(OPCIONES_MENU_PRINCIPAL):
                        opcion_seleccionada = 0 
                
                elif event.key == pygame.K_RETURN:
                    opcion_ejecutada = True
            
            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    rectangulos = dibujar_menu_principal(screen, OPCIONES_MENU_PRINCIPAL, opcion_seleccionada, contador_parpadeo, imagen_fondo)
                    
                    # Verificamos que el mouse colisione con los rectangulos
                    for i in range(len(rectangulos)):
                        rect = rectangulos[i]
                        if rect.collidepoint(event.pos): #colision del puntero con el rectangulo
                            opcion_seleccionada = i  # Cambiar a la opción clickeada
                            opcion_ejecutada = True  
                            break
            
            if opcion_ejecutada:
                if OPCIONES_MENU_PRINCIPAL[opcion_seleccionada] == "JUGAR" or OPCIONES_MENU_PRINCIPAL[opcion_seleccionada] == "SALIR":
                    detener_musica()
                return OPCIONES_MENU_PRINCIPAL[opcion_seleccionada]

        
        contador_parpadeo += 1
        
        # Efecto hover para el mouse
        rectangulos = dibujar_menu_principal(screen, OPCIONES_MENU_PRINCIPAL, opcion_seleccionada, contador_parpadeo, imagen_fondo)
        if rectangulos:
            for i in range(len(rectangulos)):
                rect = rectangulos[i]
                if rect.collidepoint(pos_mouse):
                    opcion_seleccionada = i
                    break
       
        pygame.display.flip()
        clock.tick(FPS)

def manejar_estado_menu_principal(screen, clock, imagenes):
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

def dibujar_game_over(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo_final, puntuacion=0):
    """Dibuja la pantalla de game over"""
    font_subtitulo = pygame.font.Font(None, 48)
    font_botones = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)

    
    # Dibuja fondo (igual que el menú principal)
    screen.blit(imagen_fondo_final, (0, 0))
    
    puntuacion_texto = font_subtitulo.render(f"Puntuación Final: {puntuacion}", True, COLOR_AMARILLO)
    punt_x = SCREEN_WIDTH // 2 - puntuacion_texto.get_width() // 2
    screen.blit(puntuacion_texto, (punt_x, 180))
    
    # Mensaje motivacional de fin del juego
    mensajes = [
        "¡Los invasores han ganado esta vez! " " ¡Pero la Tierra aún tiene esperanza!"
        ,
        "¿Intentarás defender el planeta otra vez?"
    ]
    for i in range(len(mensajes)):
        texto = font_small.render(mensajes[i], True, COLOR_GRIS)
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
                color = COLOR_AMARILLO
            else:
                color = COLOR_BLANCO
        else:
            color = COLOR_BLANCO
        
        texto = font_botones.render(opcion, True, color)
        x = SCREEN_WIDTH // 2 - texto.get_width() // 2
        y = y_start + i * 50
        #creacion de los rectangulos
        rect = pygame.Rect(x - 50 , y - 10, texto.get_width() + 100, texto.get_height() + 20)
        rectangulos.append(rect)
        # DIibujo test de cada rectangulo
        # if i == opcion_seleccionada:
        #     pygame.draw.rect(screen, (255, 255, 0), rect, 3)  # Amarillo para seleccionado
        # else:
        #     pygame.draw.rect(screen, (255, 0, 0), rect, 2)     # Rojo para no seleccionado
        

        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, COLOR_AMARILLO)
            screen.blit(indicador, (x - 40, y))
        
        screen.blit(texto, (x, y))
    
    # Instrucciones PARA navegar en el menu 
    instruccion = font_small.render("Usa UP/DOWN para navegar, ENTER para seleccionar", 
                                   True, COLOR_VERDE)
    instr_x = SCREEN_WIDTH // 2 - instruccion.get_width() // 2
    screen.blit(instruccion, (instr_x, SCREEN_HEIGHT - 30))

    return rectangulos

def pantalla_game_over(screen, clock, imagen_fondo_final, puntuacion=0):
    """Pantalla de fin del juego"""
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
                        opcion_seleccionada = len(OPCIONES_GAME_OVER) - 1
                elif event.key == pygame.K_DOWN:
                    opcion_seleccionada = opcion_seleccionada + 1
                    if opcion_seleccionada >= len(OPCIONES_GAME_OVER):
                        opcion_seleccionada = 0
                elif event.key == pygame.K_RETURN:
                    opcion_ejecutada = True
            
            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    rectangulos = dibujar_game_over(screen, OPCIONES_GAME_OVER, opcion_seleccionada, contador_parpadeo, imagen_fondo_final, puntuacion)
                    
                    # Verificamos que el mouse colisione con los rectangulos
                    for i in range(len(rectangulos)):
                        rect = rectangulos[i]
                        if rect.collidepoint(event.pos):
                            opcion_seleccionada = i  # Cambiar a la opción clickeada
                            opcion_ejecutada = True  
                            break
            
            if opcion_ejecutada:
                if OPCIONES_GAME_OVER[opcion_seleccionada] == "REINTENTAR" or OPCIONES_GAME_OVER[opcion_seleccionada] == "SALIR":
                    detener_musica()
                return OPCIONES_GAME_OVER[opcion_seleccionada]
        
        contador_parpadeo += 1
        
        # Efecto hover para el mouse
        rectangulos = dibujar_game_over(screen, OPCIONES_GAME_OVER, opcion_seleccionada, contador_parpadeo, imagen_fondo_final, puntuacion)
        if rectangulos:
            for i in range(len(rectangulos)):
                rect = rectangulos[i]
                if rect.collidepoint(pos_mouse):
                    opcion_seleccionada = i
                    break
        
        pygame.display.flip()
        clock.tick(FPS)
 
def manejar_estado_gameover(screen, clock, imagenes, puntuacion):
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

def manejar_estado_juego(screen, clock, imagenes):
    resultado = pantalla_juego(screen, clock, imagenes['fondos']['juego'])

    if type(resultado) == tuple:
        estado, puntuacion = resultado
        
        match estado:
            case "GAME_OVER":
                # Verificar si el puntaje obtenido en el juego es un nuevorecord
                if es_nuevo_record(puntuacion):
                    return ESTADO_NUEVO_RECORD, puntuacion
                else:
                    return ESTADO_GAME_OVER, puntuacion
            case "MENU":
                return ESTADO_MENU, 0
            case "SALIR":
                return None, 0
            case _:
                return ESTADO_JUEGO, puntuacion
    else:
        match resultado:
            case "MENU":
                return ESTADO_MENU, 0
            case "SALIR":
                return None, 0
            case _:
                return ESTADO_JUEGO, 0

def pantalla_intro(screen, clock, imagenes):
    tiempo_imagen = DURACION_INTRO
    font_skipear = pygame.font.Font(None, 26)
    font_narracion = pygame.font.Font(None, 32)

    textos_intro = [
        "Los gatos vivían en paz, disfrutando del atún, la lana y la compañía.",
        "Pero desde el espacio, un ejército de perros robots planea una invasión.",
        "Los perros atacaron la ciudad... ¡y solo un gato se atrevió a defenderla!",
        "Vos sos el Capitán Gato. ¡La misión comienza ahora!"
    ]

    # Reproduce la música solo si no se está reproduciendo aún
    reproducir_musica_si_necesario(RUTA_MUSICA_INTRO, VOLUMEN_MUSICA_INTRO)

    for i in range(1, 5):
        clave_imagen = f'img{i}'
        imagen_actual = imagenes[clave_imagen]
        texto_actual = textos_intro[i - 1]

        tiempo_inicio = pygame.time.get_ticks()

        while pygame.time.get_ticks() - tiempo_inicio < tiempo_imagen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    detener_musica()
                    return "SALIR"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    detener_musica()
                    return "SALTAR"

            screen.blit(imagen_actual, (0, 0))

            texto_render = font_narracion.render(texto_actual, True, (255, 255, 255))
            screen.blit(texto_render, (40, SCREEN_HEIGHT - 100))

            texto_skipear = font_skipear.render("Presiona SPACE para saltar la intro", True, COLOR_VERDE)
            texto_x = SCREEN_WIDTH - texto_skipear.get_width() - 20
            texto_y = SCREEN_HEIGHT - texto_skipear.get_height() - 20
            screen.blit(texto_skipear, (texto_x, texto_y))

            pygame.display.flip()
            clock.tick(FPS)

    detener_musica()
    return "COMPLETADA"

def manejar_estado_intro(screen, clock, imagenes):
    resultado = pantalla_intro(screen, clock, imagenes['intro'])

    match resultado:
        case "COMPLETADA":
            return ESTADO_MENU, 0
        case "SALTAR":
            return ESTADO_MENU, 0
        case "SALIR":
            return None, 0
        case _:
            return ESTADO_MENU, 0
    
def pantalla_juego(screen, clock, imagen_pantalla_juego):
    """Pantalla de juego con estructura"""
    
    font_small = pygame.font.Font(None, 32)
    contador_vidas = 3
    contador_puntaje = 0
    
    # Música y sonidos
    cargar_musica("assets/sounds/music/game_music.ogg")
    reproducir_musica(volumen=0.1)
    sonido_disparo = pygame.mixer.Sound(RUTA_SONIDO_DISPARO)
    sonido_disparo.set_volume(VOLUMEN_SONIDO_DISPARO)
    sonido_maullido = pygame.mixer.Sound(RUTA_SONIDO_MAULLIDO_GATO)
    sonido_maullido.set_volume(VOLUMEN_SONIDO_MAULLIDO_GATO)
    
    # Crear entidades
    imagen_jugador, rect_jugador, velocidad_jugador = crear_jugador(screen.get_width(), screen.get_height())
    balas = []
    disparar = False
    enemigos = crear_objetos(crear_enemigo, 90)
    enemigos2 = [] 
    enemigos2_creados = False
    atunes = crear_objetos(crear_atun, 15)
    milks = crear_objetos(crear_milk, 10)

    #Toma el tiempo al inicio del juego en milisegundos
    tiempo_inicio = pygame.time.get_ticks()  
    
    doble_disparo_activo = False
    doble_disparo_timer = 0

    # Parpadeo del jugador al tocar un enemigo
    jugador_parpadeando = False
    inicio_parpadeo = 0
    duracion_parpadeo = 1000  # en milisegundos


    juego_activo = 1
    while juego_activo:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
        
        keys = pygame.key.get_pressed()
        mover_jugador(rect_jugador, keys, screen.get_width(), screen.get_height(), velocidad_jugador)
        
        # Tiempo actual
        tiempo_actual = pygame.time.get_ticks()
        segundos_transcurridos = (tiempo_actual - tiempo_inicio) // 1000
        
        # Disparos
        if keys[pygame.K_SPACE]:
            if not disparar:
                sonido_disparo.play()

                if doble_disparo_activo:
                    # Crear DOS balas
                    nuevas_balas = crear_doblebala(rect_jugador.centerx, rect_jugador.top)
                    balas.extend(nuevas_balas)  # Agregar ambas balas a la lista
                else:
                    # Disparo normal (UNA bala)
                    imagen_bala, rect_bala, velocidad_bala = crear_bala(rect_jugador.centerx, rect_jugador.top)
                    balas.append((imagen_bala, rect_bala, velocidad_bala))
                
                disparar = True
        else:
            disparar = False

        #logica del doble disparo
        if doble_disparo_activo:
            doble_disparo_timer -= 1
            if doble_disparo_timer <= 0:
                doble_disparo_activo = False
        
        for bala in balas[:]:
            imagen, rect, velocidad = bala
            mover_bala(rect, velocidad)
            if bala_fuera_de_pantalla(rect):
                balas.remove(bala)
        
        # Despues de 60 segundos aparecen enemigos con mas resistencia 
        if segundos_transcurridos > 60 and not enemigos2_creados:
            enemigos2 = crear_objetos(crear_enemigo2, 10) 
            enemigos2_creados = True   
        
        # Deteccion de colisiones
        resultados_colision = procesar_todas_las_colisiones(
            rect_jugador, balas, enemigos, atunes, milks
        )
        
        # Daño al jugador (solo si no está parpadeando)
        if resultados_colision["jugador_golpeado"] and not jugador_parpadeando:
            contador_vidas -= 1
            jugador_parpadeando = True
            inicio_parpadeo = pygame.time.get_ticks()
            sonido_maullido.play()

        # Siempre se procesan los enemigos y power-ups
        if resultados_colision["enemigo_eliminado"]:
            contador_puntaje += 100

        if resultados_colision["powerup"]:
            if resultados_colision["powerup"] == "ATUN":
                contador_puntaje += 500
                doble_disparo_activo = True
                doble_disparo_timer = 600
            elif resultados_colision["powerup"] == "MILK":
                contador_vidas += 1
        
        # Verificar fin del juego
        if contador_vidas <= 0:
            detener_musica()
            return "GAME_OVER", contador_puntaje
        
        screen.blit(imagen_pantalla_juego, (0, 0))

        controlar_max_objetos_totales(enemigos, enemigos2, atunes, milks, segundos_transcurridos)
       
        # Actualizar enemigos
        for enemigo in enemigos:
            caer_objeto(enemigo)
            if enemigo["activo"]:
                screen.blit(imagen_enemigo1_escalada, (enemigo["x"], enemigo["y"]))

        for enemigo2 in enemigos2:
            caer_objeto(enemigo2)
            if enemigo2["activo"]:
                screen.blit(imagen_enemigo2_escalada, (enemigo2["x"], enemigo2["y"]))        
        
        # Actualizar power-ups
        for atun in atunes:
            caer_objeto(atun)
            if atun["activo"]:
                screen.blit(atun_escalada, (atun["x"], atun["y"]))   

        for milk in milks:
            caer_objeto(milk)
            if milk["activo"]:
                screen.blit(milk_escalada, (milk["x"], milk["y"]))        
        
        # Dibujar jugador con parpadeo
        tiempo_actual = pygame.time.get_ticks()
        if jugador_parpadeando:
            if tiempo_actual - inicio_parpadeo > duracion_parpadeo:
                jugador_parpadeando = False
                dibujar_jugador(screen, imagen_jugador, rect_jugador)
            else:
                if (tiempo_actual // 100) % 2 == 0:
                    dibujar_jugador(screen, imagen_jugador, rect_jugador)
        else:
            dibujar_jugador(screen, imagen_jugador, rect_jugador)

        # Balas
        for bala in balas:
            imagen, rect, _ = bala
            dibujar_bala(screen, imagen, rect)

        status = [f"Vidas: {contador_vidas}", f"Puntaje: {contador_puntaje}"]
        if doble_disparo_activo:
            tiempo_restante = doble_disparo_timer // 60  # Convertir los frames a segundos
            status.append(f"DOBLE DISPARO: {tiempo_restante}s")
        
        for i in range(len(status)):
            texto = font_small.render(status[i], True, COLOR_VERDE)
            screen.blit(texto, (20, 20 + i * 35))
        
        # Debug con cuadrados - Hay que sacarlo en la version final!! 
        # dibujar_rectangulos_debug(screen, rect_jugador, enemigos, balas)
        
        pygame.display.flip()
        clock.tick(FPS)

def dibujar_rectangulos_debug(screen, rect_jugador, enemigos, balas):
    """
    Dibuja rectángulos para debug
    - Jugador: Amarillo
    - Enemigos: Rojo  
    - Balas: Verde
    """
    pygame.draw.rect(screen, (255, 255, 0), rect_jugador, 3)
    
    for enemigo in enemigos:
        if enemigo["activo"]:
            rect_enemigo = pygame.Rect(enemigo["x"], enemigo["y"], 85, 85)
            pygame.draw.rect(screen, (255, 0, 0), rect_enemigo, 3)
    
    for bala in balas:
        if isinstance(bala, tuple) and len(bala) >= 2:
            rect_bala = bala[1]
            pygame.draw.rect(screen, (0, 255, 0), rect_bala, 3) 


def detectar_colisiones_perros(rect_jugador, enemigos):
    """
    Detecta colisiones entre el jugador y los enemigos.
    Retorna True si hay colisión, False en caso contrario.
    """
    for enemigo in enemigos[:]:  # Usar copia de la lista
        if enemigo["activo"]:
            rect_enemigo = pygame.Rect(enemigo["x"], enemigo["y"], 85, 85)
            
            if rect_jugador.colliderect(rect_enemigo):
                enemigos.remove(enemigo)
                print(f"Enemigos restantes: {len(enemigos)}")
                return True
    
    return False

def detectar_colision_balas(balas, enemigos):
    """
    Detecta colisiones entre balas y enemigos.
    Elimina tanto las balas como los enemigos que colisionan.
    """
    for bala in balas[:]:  # Usar copia de la lista de balas
        imagen_bala, rect_bala, velocidad_bala = bala
        
        for enemigo in enemigos[:]:  # Usar copia de la lista de enemigos
            if enemigo["activo"]:
                rect_enemigo = pygame.Rect(enemigo["x"], enemigo["y"], 85, 85)
                
                if rect_bala.colliderect(rect_enemigo):
                    
                    balas.remove(bala)
                    enemigos.remove(enemigo)
                    print(f"Enemigos restantes: {len(enemigos)}")
                    
                    return True
    
    return False

def detectar_colision_jugador_powerups(rect_jugador, atunes, milks):
    """
    Detecta colisiones entre el jugador y power-ups.
    Retorna el tipo de power-up recolectado o None.
    """
    for atun in atunes[:]:
        if atun["activo"]:
            rect_atun = pygame.Rect(atun["x"], atun["y"], 85, 85)
            
            if rect_jugador.colliderect(rect_atun):
                atunes.remove(atun)
                return "ATUN"
    
    for milk in milks[:]:
        if milk["activo"]:
            rect_milk = pygame.Rect(milk["x"], milk["y"], 85, 85)
            
            if rect_jugador.colliderect(rect_milk):
                milks.remove(milk)
                return "MILK"
    
    return None  # No hubo colisión con power-ups

def procesar_todas_las_colisiones(rect_jugador, balas, enemigos, atunes, milks):
    """
    Función principal que maneja todas las colisiones del juego.
    """
    colision_jugador = detectar_colisiones_perros(rect_jugador, enemigos)
    
    colision_balas = detectar_colision_balas(balas, enemigos)
    
    powerup_recolectado = detectar_colision_jugador_powerups(rect_jugador, atunes, milks)
    
    # Retornar resultados para que el juego principal pueda saber que paso
    return {
        "jugador_golpeado": colision_jugador,
        "enemigo_eliminado": colision_balas,
        "powerup": powerup_recolectado
    }


def crear_doblebala(x,y):
    """
    Crea dos balas: una a la izquierda y otra a la derecha del jugador.
    """
    imagen_bala1, rect_bala1, velocidad_bala1 = crear_bala(x - 15, y)
    imagen_bala2, rect_bala2, velocidad_bala2 = crear_bala(x + 15, y)
    
    return [(imagen_bala1, rect_bala1, velocidad_bala1), (imagen_bala2, rect_bala2, velocidad_bala2)]


def pantalla_nuevo_record(screen, clock, imagen_record, puntuacion, nombre_jugador):    
    # Reproducir música de game over (por ahora)
    reproducir_musica_si_necesario(RUTA_MUSICA_GAME_OVER, VOLUMEN_GAME_OVER)
    
    opcion_seleccionada = 0
    contador_parpadeo = 0
    
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
                        opcion_seleccionada = len(OPCIONES_RECORD) - 1
                elif event.key == pygame.K_DOWN:
                    opcion_seleccionada = opcion_seleccionada + 1
                    if opcion_seleccionada >= len(OPCIONES_RECORD):
                        opcion_seleccionada = 0
                elif event.key == pygame.K_RETURN:
                    opcion_ejecutada = True
            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    rectangulos = dibujar_pantalla_nuevo_record(screen, OPCIONES_RECORD, opcion_seleccionada, contador_parpadeo, imagen_record, puntuacion, nombre_jugador)
                    
                    # Verificamos que el mouse colisione con los rectangulos
                    for i in range(len(rectangulos)):
                        rect = rectangulos[i]
                        if rect.collidepoint(event.pos):
                            opcion_seleccionada = i  # Cambiar a la opción clickeada
                            opcion_ejecutada = True  
                            break

            
            if opcion_ejecutada:
                if OPCIONES_RECORD[opcion_seleccionada] in ["JUGAR OTRA VEZ", "SALIR"]:
                    detener_musica()
                return OPCIONES_RECORD[opcion_seleccionada]
        
        contador_parpadeo += 1
        
        screen.blit(imagen_record, (0, 0))
        
        # Overlay semi-transparente
        # overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # overlay.set_alpha(120)
        # overlay.fill((0, 0, 0))
        # screen.blit(overlay, (0, 0))
        
        # Efecto hover para el mouse
        rectangulos = dibujar_pantalla_nuevo_record(screen, OPCIONES_RECORD, opcion_seleccionada, contador_parpadeo, imagen_record, puntuacion, nombre_jugador)
        if rectangulos:
            for i in range(len(rectangulos)):
                rect = rectangulos[i]
                if rect.collidepoint(pos_mouse):
                    opcion_seleccionada = i
                    break
        pygame.display.flip()
        clock.tick(FPS)

def dibujar_pantalla_nuevo_record(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_record, puntuacion, nombre_jugador):
    """Dibuja la pantalla de nuevo récord - VERSIÓN CON DEBUG"""
    font_subtitulo = pygame.font.Font(None, 48)
    font_botones = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)

    screen.blit(imagen_record, (0, 0))
    

    # Mostrar nombre y puntuación
    texto_jugador = font_subtitulo.render(f"Piloto: {nombre_jugador}", True, COLOR_VERDE)
    jugador_x = SCREEN_WIDTH // 2 - texto_jugador.get_width() // 2
    screen.blit(texto_jugador, (jugador_x, 160))
    
    texto_puntaje = font_subtitulo.render(f"Puntuación Final: {puntuacion}", True, COLOR_BLANCO)
    puntaje_x = SCREEN_WIDTH // 2 - texto_puntaje.get_width() // 2
    screen.blit(texto_puntaje, (puntaje_x, 200))
    
    # Mensaje de felicitación
    mensaje = "¡Eres el mejor defensor del planeta!"
    texto_mensaje = font_small.render(mensaje, True, COLOR_GRIS)
    mensaje_x = SCREEN_WIDTH // 2 - texto_mensaje.get_width() // 2
    screen.blit(texto_mensaje, (mensaje_x, 250))

    # Opciones del menú
    y_start = 320
    rectangulos = []
    
    for i in range(len(opciones)):
        opcion = opciones[i]
        
        
        # Parpadeo de la opción seleccionada
        if i == opcion_seleccionada:
            if contador_parpadeo % 30 < 15:
                color = COLOR_AMARILLO
            else:
                color = COLOR_BLANCO
        else:
            color = COLOR_BLANCO

        texto = font_botones.render(opcion, True, color)
        x = SCREEN_WIDTH // 2 - texto.get_width() // 2
        y = y_start + i * 50
        

        rect = pygame.Rect(x - 50, y - 10, texto.get_width() + 100, texto.get_height() + 20)
        rectangulos.append(rect)
        
        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, COLOR_AMARILLO)
            screen.blit(indicador, (x - 40, y))
        
        screen.blit(texto, (x, y))

    return rectangulos

def manejar_estado_nuevo_record(screen, clock, imagenes, puntuacion):
    """Maneja el estado de nuevo récord - PANTALLA FINAL"""
    
    nombre_jugador = pantalla_nuevo_record_solo_guardar(screen, clock, imagenes['fondos']['victoria'], puntuacion)
    
    salir = False
    while not salir:
        resultado = pantalla_nuevo_record(screen, clock, imagenes['fondos']['victoria'], puntuacion, nombre_jugador)
        
        match resultado:
            case "JUGAR OTRA VEZ":
                return ESTADO_JUEGO, 0
            case "RANKING":
                resultado_ranking = mostrar_modal_puntuaciones(screen, clock, imagenes['fondos']['victoria'])
                if resultado_ranking == "SALIR":
                    return None, 0
                continue
            case "MENU PRINCIPAL":
                return ESTADO_MENU, 0
            case "SALIR":
                return None, 0
            case _:
                return ESTADO_MENU, 0
        
def pantalla_nuevo_record_solo_guardar(screen, clock, imagen_record, puntuacion):
    """SOLO pide nombre y guarda - se ejecuta UNA VEZ"""
    
    # Obtener nombre del jugador
    nombre_jugador = obtener_nombre_jugador(screen, clock, imagen_record)
    
    # Guardar la puntuación en el CSV
    agregar_puntuacion_csv(nombre_jugador, puntuacion)
        
    return nombre_jugador 