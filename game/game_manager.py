# Archivo de configuraciones a cargo de León! 

import pygame
from config import *
from utils import  cargar_musica, reproducir_musica, detener_musica, mostrar_modal_puntuaciones, mostrar_modal_creditos, reproducir_musica_si_necesario, es_nuevo_record, agregar_puntuacion_csv, obtener_nombre_jugador
from game.player import crear_jugador, mover_jugador, dibujar_jugador
from game.bullet import crear_bala, mover_bala, dibujar_bala, bala_fuera_de_pantalla, crear_doblebala
from game.enemies import crear_enemigo, crear_enemigo2, imagen_enemigo1_escalada, imagen_enemigo2_escalada
from game.powerups import crear_atun, crear_milk, atun_escalada, milk_escalada
from utils import crear_objetos, caer_objeto

def verificar_enemigos_en_piso(enemigos1, enemigos2, contador_puntaje):
    """
    Verifica si algún enemigo cayó al piso y aplica penalización
    Retorna: puntos perdidos
    """
    puntos_perdidos = 0
    limite_piso = SCREEN_HEIGHT - 10  # Un poco antes del borde para mejor detección
    
    #VERIFICAR ENEMIGOS1
    for enemigo in enemigos1[:]:  # Usar copia para poder modificar la lista
        if enemigo["activo"] and enemigo["y"] >= limite_piso:
            puntos_perdidos += 150
            enemigo["activo"] = False  # Desactivar el enemigo
    
    #VERIFICAR ENEMIGOS2
    for enemigo2 in enemigos2[:]:
        if enemigo2["activo"] and enemigo2["y"] >= limite_piso:
            puntos_perdidos += 1000  # Más puntos porque son más peligrosos
            enemigo2["activo"] = False
    
    return puntos_perdidos

def dibujar_menu_principal(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo):
    """Dibuja el menú principal del juego"""
    font_botones = pygame.font.SysFont("impact", 48)
    
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
    font_botones = pygame.font.SysFont("impact", 36)
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

        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, COLOR_AMARILLO)
            screen.blit(indicador, (x - 40, y))
        
        screen.blit(texto, (x, y))
    
    # Instrucciones PARA navegar en el menu 
    # instruccion = font_small.render("Usa UP/DOWN para navegar, ENTER para seleccionar", 
    #                                True, COLOR_VERDE)
    # instr_x = SCREEN_WIDTH // 2 - instruccion.get_width() // 2
    # screen.blit(instruccion, (instr_x, SCREEN_HEIGHT - 30))

    return rectangulos

def pantalla_game_over(screen, clock, imagen_fondo_final, puntuacion=0):
    """Pantalla de fin del juego"""
    opcion_seleccionada = 0
    contador_parpadeo = 0
    
    reproducir_musica_si_necesario(RUTA_MUSICA_GAME_OVER, VOLUMEN_GAME_OVER)

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
                # Verificar si el puntaje obtenido en el juego es un nuevo record
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
    

def gestionar_aparicion_optimizada(enemigos1, enemigos2, atunes, milks, timer_powerups, segundos):
    """Gestión optimizada con reciclaje infinito de enemigos"""
    import random
    
    # RECICLAJE DE ENEMIGOS: Reactivar enemigos que salieron de pantalla
    reciclar_enemigos_infinitos(enemigos1)
    if segundos >= 60:
        reciclar_enemigos_infinitos(enemigos2)
    
    # CONTROL DE POWER-UPS: Máximo 2 en pantalla, cada 5 segundos
    powerups_activos = sum(1 for atun in atunes if atun["activo"]) + \
                       sum(1 for milk in milks if milk["activo"])
    
    if powerups_activos < 2 and timer_powerups % 300 == 0:  # Cada 5 segundos
        if random.random() < 0.8:  # 80% probabilidad
            if random.random() < 0.7:  # 70% atún, 30% milk
                activar_objeto_aleatorio(atunes, "🐟 ATÚN")
            else:
                activar_objeto_aleatorio(milks, "🥛 MILK")
    
    # ACTIVACIÓN FORZADA DE ENEMIGOS: Asegurar que siempre haya enemigos
    enemigos1_activos = sum(1 for e in enemigos1 if e["activo"])
    if enemigos1_activos < 6:  # Máximo 6 enemigos1
        forzar_activacion_enemigos(enemigos1, 6 - enemigos1_activos)
    
   # ACTIVACIÓN FORZADA DE ENEMIGOS2 (después del minuto)
    if segundos >= 60:
        enemigos2_activos = sum(1 for e in enemigos2 if e["activo"])
        max_enemigos2 = min(4, (segundos - 60) // 30 + 1)  # Aumenta cada 30 seg
        
        if enemigos2_activos < max_enemigos2:
            forzar_activacion_enemigos(enemigos2, max_enemigos2 - enemigos2_activos)
    
    # Actualizar todos los objetos
    for lista in [enemigos1, enemigos2, atunes, milks]:
        for objeto in lista:
            caer_objeto(objeto)

def reciclar_enemigos_infinitos(lista_enemigos):
    """Recicla enemigos que salieron de pantalla para reutilizarlos"""
    import random
    
    for enemigo in lista_enemigos:
        # Si el enemigo está inactivo y salió de pantalla, reciclarlo
        if not enemigo["activo"] and enemigo["y"] > SCREEN_HEIGHT + 100:
            # RESETEAR ENEMIGO para reutilizarlo
            enemigo["x"] = random.randint(0, SCREEN_WIDTH - 85)
            enemigo["y"] = random.randint(-300, -50)
            enemigo["velocidad_y"] = random.randint(3, 6)
            enemigo["tiempo_espera"] = random.randint(0, 120)  # Tiempo corto para reaparecer
            
            # Resetear vida para enemigos2
            if "vida" in enemigo:
                enemigo["vida"] = 2

def forzar_activacion_enemigos(lista_enemigos, cantidad_necesaria):
    """Fuerza la activación de enemigos si no hay suficientes"""
    import random
    
    activados = 0
    intentos = 0
    max_intentos = len(lista_enemigos)
    
    while activados < cantidad_necesaria and intentos < max_intentos:
        for enemigo in lista_enemigos:
            if not enemigo["activo"]:
                # ACTIVAR INMEDIATAMENTE sin esperar tiempo_espera
                enemigo["activo"] = True
                enemigo["tiempo_espera"] = 0
                
                # Si el enemigo está muy abajo, reposicionarlo
                if enemigo["y"] > 0:
                    enemigo["y"] = random.randint(-200, -50)
                    enemigo["x"] = random.randint(0, SCREEN_WIDTH - 85)
                
                activados += 1
                
                if activados >= cantidad_necesaria:
                    break
        
        intentos += 1


def activar_objeto_aleatorio(lista_objetos, nombre):
    """Activa un objeto aleatorio de la lista"""
    for objeto in lista_objetos:
        if not objeto["activo"]:
            objeto["activo"] = True
            objeto["tiempo_espera"] = 0
            break

def activar_enemigos_gradual(lista_enemigos, cantidad):
    """Activa enemigos gradualmente"""
    activados = 0
    for enemigo in lista_enemigos:
        if not enemigo["activo"] and enemigo["tiempo_espera"] <= 0:
            enemigo["activo"] = True
            activados += 1
            if activados >= cantidad:
                break

# ===== SISTEMA DE COLISIONES COMPLETO =====

def procesar_colisiones_completas(rect_jugador, balas, enemigos1, enemigos2, atunes, milks):
    """Procesa todas las colisiones con lógica de 2 disparos para enemigos2"""
    
    puntos_ganados = 0
    
    # Colisiones jugador vs enemigos
    colision_jugador1 = detectar_colision_jugador_vs_enemigos(rect_jugador, enemigos1)
    colision_jugador2 = detectar_colision_jugador_vs_enemigos(rect_jugador, enemigos2)
    
    # Colisiones balas vs enemigos1 (1 disparo)
    if detectar_colision_balas_vs_enemigos1(balas, enemigos1):
        puntos_ganados += 100
    
    # Colisiones balas vs enemigos2 (2 disparos)
    puntos_enemigos2 = detectar_colision_balas_vs_enemigos2(balas, enemigos2)
    puntos_ganados += puntos_enemigos2
    
    # Colisiones con power-ups
    powerup_recolectado = detectar_colision_jugador_powerups(rect_jugador, atunes, milks)
    
    return {
        "jugador_golpeado": colision_jugador1 or colision_jugador2,
        "puntos_ganados": puntos_ganados,
        "powerup": powerup_recolectado
    }

def detectar_colision_jugador_vs_enemigos(rect_jugador, enemigos):
    """Detecta colisión jugador vs cualquier tipo de enemigos"""
    for enemigo in enemigos[:]:
        if enemigo["activo"]:
            rect_enemigo = pygame.Rect(enemigo["x"], enemigo["y"], 85, 85)
            if rect_jugador.colliderect(rect_enemigo):
                enemigos.remove(enemigo)
                return True
    return False

def detectar_colision_balas_vs_enemigos1(balas, enemigos1):
    """Detecta colisiones balas vs enemigos1 (mueren en 1 disparo)"""
    for bala in balas[:]:
        imagen_bala, rect_bala, velocidad_bala = bala
        
        for enemigo in enemigos1[:]:
            if enemigo["activo"]:
                rect_enemigo = pygame.Rect(enemigo["x"], enemigo["y"], 85, 85)
                
                if rect_bala.colliderect(rect_enemigo):
                    balas.remove(bala)
                    enemigos1.remove(enemigo)
                    return True
    return False

def detectar_colision_balas_vs_enemigos2(balas, enemigos2):
    """Detecta colisiones balas vs enemigos2 (requieren 2 disparos)"""
    puntos = 0
    
    for bala in balas[:]:
        imagen_bala, rect_bala, velocidad_bala = bala
        
        for enemigo2 in enemigos2[:]:
            if enemigo2["activo"]:
                rect_enemigo = pygame.Rect(enemigo2["x"], enemigo2["y"], 85, 85)
                
                if rect_bala.colliderect(rect_enemigo):
                    balas.remove(bala)
                    
                    # LÓGICA DE 2 DISPAROS
                    if "vida" not in enemigo2:
                        enemigo2["vida"] = 2  # Inicializar vida
                    
                    enemigo2["vida"] -= 1
                    
                    if enemigo2["vida"] <= 0:
                        # Enemigo eliminado
                        enemigos2.remove(enemigo2)
                        puntos += 200  # Más puntos por ser más difícil
                    else:
                        # Enemigo herido
                        puntos += 50   # Puntos por herir
                    
                    break
    
    return puntos

def dibujar_ui_optimizada(screen, font, vidas, puntaje, doble_disparo_activo, doble_disparo_timer, segundos, icono_doble_disparo=None):
    status = [
        f"Vidas: {vidas}",
        f"Puntaje: {puntaje}",
        f"Tiempo: {segundos}s"
    ]
    
    for i in range(len(status)):
        color = COLOR_VERDE if i < 3 else COLOR_AMARILLO
        texto = font.render(status[i], True, color)
        screen.blit(texto, (20, 20 + i * 35))
    
    y_siguiente = 20 + len(status) * 35
    
    if doble_disparo_activo:
        tiempo_restante = doble_disparo_timer // 60
        
        if icono_doble_disparo:
            screen.blit(icono_doble_disparo, (20, y_siguiente))
        
        texto_doble = font.render(f" DOBLE DISPARO: {tiempo_restante}s", True, COLOR_AMARILLO)
        screen.blit(texto_doble, (35, y_siguiente))
        y_siguiente += 35
    
    # MENSAJE DE MODO DIFÍCIL (siempre debajo del power-up si existe)
    if segundos >= 60:
        texto_dificil = font.render("MODO DIFÍCIL ACTIVADO", True, COLOR_ROJO)
        screen.blit(texto_dificil, (20, y_siguiente))

# def dibujar_rectangulos_debug(screen, rect_jugador, enemigos, balas):
#     """
#     Dibuja rectángulos para debug
#     - Jugador: Amarillo
#     - Enemigos: Rojo  
#     - Balas: Verde
#     """
#     pygame.draw.rect(screen, (255, 255, 0), rect_jugador, 3)
    
#     for enemigo in enemigos:
#         if enemigo["activo"]:
#             rect_enemigo = pygame.Rect(enemigo["x"], enemigo["y"], 85, 85)
#             pygame.draw.rect(screen, (255, 0, 0), rect_enemigo, 3)
    
#     for bala in balas:
#         if isinstance(bala, tuple) and len(bala) >= 2:
#             rect_bala = bala[1]
#             pygame.draw.rect(screen, (0, 255, 0), rect_bala, 3) 


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

def pantalla_nuevo_record(screen, clock, imagen_record, puntuacion, nombre_jugador):    
    cargar_musica(RUTA_MUSICA_RECORD)
    reproducir_musica(VOLUMEN_MUSICA_RECORD)
    
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
    font_botones = pygame.font.SysFont("impact", 36)
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
    texto_mensaje = font_small.render(mensaje, True, COLOR_BLANCO)
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



def gestionar_aparicion_continua(enemigos1, enemigos2, atunes, milks, timer_powerups, segundos):
    """Sistema de aparición continua - NUNCA se agotan los enemigos"""
    import random
    
    # RECICLAJE AGRESIVO: Enemigos que salen de pantalla se reciclan inmediatamente
    reciclar_enemigos_agresivo(enemigos1)
    if segundos >= 60:
        reciclar_enemigos_agresivo(enemigos2)
    
    # CREACIÓN DINÁMICA: Si se agotan enemigos, crear más inmediatamente
    asegurar_stock_enemigos(enemigos1, enemigos2, segundos)
    
    # CONTROL DE POWER-UPS 
    gestionar_powerups_controlado(atunes, milks, timer_powerups)
    
    # ACTIVACIÓN CONTINUA DE ENEMIGOS
    if segundos < 60:
        # PRIMER MINUTO: Solo enemigos1, pero SIEMPRE presentes
        mantener_enemigos_activos(enemigos1, cantidad_minima=8, cantidad_maxima=12)
    else:
        # DESPUÉS DEL MINUTO: Mix de enemigos1 y enemigos2
        mantener_enemigos_activos(enemigos1, cantidad_minima=6, cantidad_maxima=10)
        mantener_enemigos_activos(enemigos2, cantidad_minima=2, cantidad_maxima=5)
    
    # ACTUALIZAR TODOS LOS OBJETOS
    actualizar_todos_los_objetos(enemigos1, enemigos2, atunes, milks)

def reciclar_enemigos_agresivo(lista_enemigos):
    """Reciclaje inmediato y agresivo de enemigos"""
    import random
    
    for enemigo in lista_enemigos:
        # Condiciones para reciclar:
        # No está activo Y (salió de pantalla O tiene tiempo de espera alto)
        if not enemigo["activo"] and (enemigo["y"] > SCREEN_HEIGHT + 50 or enemigo["tiempo_espera"] > 300):
            # RESETEO COMPLETO E INMEDIATO
            enemigo["x"] = random.randint(0, SCREEN_WIDTH - 85)
            enemigo["y"] = random.randint(-400, -50)
            enemigo["velocidad_y"] = random.randint(3, 6)
            enemigo["tiempo_espera"] = random.randint(0, 60)  # ⚡ Tiempo muy corto
            enemigo["activo"] = False  # Se activará por el sistema normal
            
            # Resetear vida para enemigos2
            if "vida" in enemigo:
                enemigo["vida"] = 2

def asegurar_stock_enemigos(enemigos1, enemigos2, segundos):
    """Asegura que siempre haya suficientes enemigos disponibles"""
    
    # CONTAR ENEMIGOS1 DISPONIBLES (activos + inactivos reciclables)
    enemigos1_disponibles = len([e for e in enemigos1 
                                if not e["activo"] and e["y"] <= SCREEN_HEIGHT + 50])
    
    if enemigos1_disponibles < 20:  # Si quedan pocos disponibles
        nuevos_enemigos1 = crear_objetos(crear_enemigo, 50)
        enemigos1.extend(nuevos_enemigos1)
    
    # LO MISMO PARA ENEMIGOS2 (solo después del minuto)
    if segundos >= 60:
        enemigos2_disponibles = len([e for e in enemigos2 
                                    if not e["activo"] and e["y"] <= SCREEN_HEIGHT + 50])
        
        if enemigos2_disponibles < 10:
            nuevos_enemigos2 = crear_objetos(crear_enemigo2, 30)
            enemigos2.extend(nuevos_enemigos2)

def mantener_enemigos_activos(lista_enemigos, cantidad_minima, cantidad_maxima):
    """Mantiene una cantidad específica de enemigos activos SIEMPRE"""
    import random
    
    # Contar enemigos activos
    activos = sum(1 for e in lista_enemigos if e["activo"])
    
    if activos < cantidad_minima:
        # ⚡ ACTIVACIÓN FORZADA E INMEDIATA
        necesarios = cantidad_minima - activos
        activados = 0
        
        for enemigo in lista_enemigos:
            if not enemigo["activo"]:
                # ACTIVAR INMEDIATAMENTE
                enemigo["activo"] = True
                enemigo["tiempo_espera"] = 0
                
                # Si está mal posicionado, reposicionarlo
                if enemigo["y"] > 0:
                    enemigo["y"] = random.randint(-300, -50)
                    enemigo["x"] = random.randint(0, SCREEN_WIDTH - 85)
                
                activados += 1
                if activados >= necesarios:
                    break
        

def gestionar_powerups_controlado(atunes, milks, timer_powerups):
    """Control de power-ups sin cambios"""
    import random
    
    powerups_activos = sum(1 for atun in atunes if atun["activo"]) + \
                       sum(1 for milk in milks if milk["activo"])
    
    if powerups_activos < 2 and timer_powerups % 300 == 0:  # Cada 5 segundos
        if random.random() < 0.8:  # 80% probabilidad
            if random.random() < 0.7:  # 70% atún, 30% milk
                activar_objeto_aleatorio(atunes, "🐟 ATÚN")
            else:
                activar_objeto_aleatorio(milks, "🥛 MILK")

def actualizar_todos_los_objetos(enemigos1, enemigos2, atunes, milks):
    """Actualiza el movimiento de todos los objetos"""
    for lista in [enemigos1, enemigos2, atunes, milks]:
        for objeto in lista:
            caer_objeto(objeto)


def pantalla_juego(screen, clock, imagen_pantalla_juego):
    """Pantalla de juego con enemigos continuos infinitos"""
    
    font_small = pygame.font.SysFont("consolas", 32)
    contador_vidas = 3
    contador_puntaje = 0
    
    # Música, sonidos e imagenes
    cargar_musica("assets/sounds/music/game_music.ogg")
    reproducir_musica(volumen=0.1)
    sonido_disparo = pygame.mixer.Sound(RUTA_SONIDO_DISPARO)
    sonido_disparo.set_volume(VOLUMEN_SONIDO_DISPARO)
    sonido_maullido = pygame.mixer.Sound(RUTA_SONIDO_MAULLIDO_GATO)
    sonido_maullido.set_volume(VOLUMEN_SONIDO_MAULLIDO_GATO)
    sonido_powerup = pygame.mixer.Sound(RUTA_SONIDA_POWER_UP)
    sonido_powerup.set_volume(VOLUMEN_SONIDO_POWER_UP)
    sonido_enemigo_muerto = pygame.mixer.Sound(RUTA_SONIDO_MUERTE_PERRO)
    sonido_enemigo_muerto.set_volume(VOLUMEN_SONIDO_MUERTE_PERRO)
    icono_bullets = pygame.image.load("assets/images/Balas/dobledisparo.png")
    icono_pequeno = pygame.transform.scale(icono_bullets, (24, 24))
    
    # Crear entidades
    imagen_jugador, rect_jugador, velocidad_jugador = crear_jugador(screen.get_width(), screen.get_height())
    balas = []
    disparar = False
    
    # ENEMIGOS: Stock inicial grande para asegurar continuidad
    enemigos1 = crear_objetos(crear_enemigo, 200)    # Stock grande de enemigos1
    enemigos2 = crear_objetos(crear_enemigo2, 100)   # Stock grande de enemigos2 desde el inicio
    
    # Power-ups reducidos
    atunes = crear_objetos(crear_atun, 15)
    milks = crear_objetos(crear_milk, 10)
    
    # Control de tiempo
    tiempo_inicio = pygame.time.get_ticks()
    timer_powerups = 0
    
    # Sistema de doble disparo
    doble_disparo_activo = False
    doble_disparo_timer = 0
    
    # Parpadeo del jugador
    jugador_parpadeando = False
    inicio_parpadeo = 0
    duracion_parpadeo = 1000

    juego_activo = 1
    while juego_activo:
        
        # Eventos 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
        
        # Movimiento y disparo 
        keys = pygame.key.get_pressed()
        mover_jugador(rect_jugador, keys, screen.get_width(), screen.get_height(), velocidad_jugador)
        
        tiempo_actual = pygame.time.get_ticks()
        segundos_transcurridos = (tiempo_actual - tiempo_inicio) // 1000
        
        # Sistema de disparo 
        if keys[pygame.K_SPACE]:
            if not disparar:
                sonido_disparo.play()
                if doble_disparo_activo:
                    nuevas_balas = crear_doblebala(rect_jugador.centerx, rect_jugador.top)
                    balas.extend(nuevas_balas)
                else:
                    imagen_bala, rect_bala, velocidad_bala = crear_bala(rect_jugador.centerx, rect_jugador.top)
                    balas.append((imagen_bala, rect_bala, velocidad_bala))
                disparar = True
        else:
            disparar = False

        # Lógica del doble disparo 
        if doble_disparo_activo:
            doble_disparo_timer -= 1
            if doble_disparo_timer <= 0:
                doble_disparo_activo = False
        
        # Movimiento de balas 
        for bala in balas[:]:
            imagen, rect, velocidad = bala
            mover_bala(rect, velocidad)
            if bala_fuera_de_pantalla(rect):
                balas.remove(bala)
        
        # SISTEMA CORREGIDO: Aparición continua
        gestionar_aparicion_continua(
            enemigos1, enemigos2, atunes, milks, 
            timer_powerups, segundos_transcurridos
        )
        timer_powerups += 1

        # VERIFICAR ENEMIGOS QUE TOCAN EL PISO Y APLICAR PENALIZACIÓN
        puntos_perdidos = verificar_enemigos_en_piso(enemigos1, enemigos2, contador_puntaje)
        contador_puntaje -= puntos_perdidos

        if contador_puntaje < 0:
            contador_puntaje = 0
        
        # COLISIONES: Solo usar enemigos según la fase
        if segundos_transcurridos < 60:
            # PRIMER MINUTO: Solo enemigos1
            resultados_colision = procesar_colisiones_completas(
                rect_jugador, balas, enemigos1, [], atunes, milks
            )
        else:
            # DESPUÉS DEL MINUTO: Ambos tipos
            resultados_colision = procesar_colisiones_completas(
                rect_jugador, balas, enemigos1, enemigos2, atunes, milks
            )
        
        # Resto de la lógica 
        if resultados_colision["jugador_golpeado"] and not jugador_parpadeando:
            contador_vidas -= 1
            jugador_parpadeando = True
            inicio_parpadeo = pygame.time.get_ticks()
            sonido_maullido.play()

        contador_puntaje += resultados_colision["puntos_ganados"]
        if resultados_colision["puntos_ganados"] > 0:
            sonido_enemigo_muerto.play()

        if resultados_colision["powerup"]:
            sonido_powerup.play()

        if resultados_colision["powerup"] == "ATUN":
            contador_puntaje += 500
            doble_disparo_activo = True
            doble_disparo_timer = 600

        elif resultados_colision["powerup"] == "MILK":
            contador_vidas += 1
        
        if contador_vidas <= 0:
            detener_musica()
            return "GAME_OVER", contador_puntaje
        
        # RENDERIZADO: Solo dibujar enemigos según la fase
        screen.blit(imagen_pantalla_juego, (0, 0))
        
        # Dibujar enemigos1 (siempre)
        for enemigo in enemigos1:
            if enemigo["activo"]:
                screen.blit(imagen_enemigo1_escalada, (enemigo["x"], enemigo["y"]))

        # Dibujar enemigos2 (solo después del minuto)
        if segundos_transcurridos >= 60:
            for enemigo2 in enemigos2:
                if enemigo2["activo"]:
                    if enemigo2.get("vida", 2) == 1:
                        if (pygame.time.get_ticks() // 200) % 2:
                            screen.blit(imagen_enemigo2_escalada, (enemigo2["x"], enemigo2["y"]))
                    else:
                        screen.blit(imagen_enemigo2_escalada, (enemigo2["x"], enemigo2["y"]))
        
        # Resto del renderizado 
        for atun in atunes:
            if atun["activo"]:
                screen.blit(atun_escalada, (atun["x"], atun["y"]))

        for milk in milks:
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

        # Dibujar balas 
        for bala in balas:
            imagen, rect, _ = bala
            dibujar_bala(screen, imagen, rect)

        # UI mejorada 
        dibujar_ui_optimizada(screen, font_small, contador_vidas, contador_puntaje, 
                            doble_disparo_activo, doble_disparo_timer, segundos_transcurridos, icono_pequeno)
        
        pygame.display.flip()
        clock.tick(FPS)