# Archivo de configuraciones a cargo de León! 
from config import *
import pygame
import csv
import sys
import random

def cargar_imagen_fondo(ruta_imagen):
    """Carga y escala la imagen de fondo"""
    imagen = pygame.image.load(ruta_imagen)
    imagen_escalada = pygame.transform.scale(imagen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return imagen_escalada

#manejo de juego

def iniciar_juego():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITULO_JUEGO)
    clock = pygame.time.Clock()
    icono = pygame.image.load(RUTA_ICONO_JUEGO)
    pygame.display.set_icon(icono)
    
    return screen, clock

def cargar_todas_las_imagenes():
    return {
        'intro': {
            'img1': cargar_imagen_fondo(RUTA_IMAGEN_INTRO_1),
            'img2': cargar_imagen_fondo(RUTA_IMAGEN_INTRO_2),
            'img3': cargar_imagen_fondo(RUTA_IMAGEN_INTRO_3),
            'img4': cargar_imagen_fondo(RUTA_IMAGEN_INTRO_4),
        },
        'fondos': {
            'menu': cargar_imagen_fondo(RUTA_IMAGEN_FONDO_MENU_PRINCIPAL),
            'game_over': cargar_imagen_fondo(RUTA_IMAGEN_FIN_DEL_JUEGO),
            'juego': cargar_imagen_fondo(RUTA_IMAGEN_PANTALLA_JUEGO),
            'victoria': cargar_imagen_fondo(RUTA_IMAGEN_NUEVO_RECORD),
        },
        'sprites': {
            # falta implementar imagenes de los sprites
        },
        'iconos': {
            # 'vida': pygame.image.load("assets/images/ui/vida.png"), falta implementar imagen
        }
    }

def finalizar_juego():

    pygame.quit()
    sys.exit()



# Musica del juego

def cargar_musica(ruta_musica):
    """Carga una canción"""
    pygame.mixer.music.load(ruta_musica)

def reproducir_musica(volumen, loops=-1):
    """Reproduce la música cargada"""
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(loops)  # loops=-1 significa repetir infinitamente

def detener_musica():
    """Detiene la música actual"""
    pygame.mixer.music.stop()

def esta_reproduciendo_musica():
    """Verifica si la música está reproduciéndose"""
    return pygame.mixer.music.get_busy()
def reproducir_musica_si_necesario(ruta_musica, volumen):
    """Reproduce la música si no se está reproduciendo"""
    if not esta_reproduciendo_musica():
        cargar_musica(ruta_musica)
        reproducir_musica(volumen)
    else:
        print("La música ya se está reproduciendo.")

#Funciones para manejar el archivo csv
def leer_puntuaciones_csv(archivo="assets/puntuaciones.csv"):
    """Lee las puntuaciones desde un archivo CSV"""
    puntuaciones = []
    archivo_csv = open(archivo, 'r', encoding='utf-8') #aca abro el archivo en modo lectura 'r' con la codificcion UTF8
    lector = csv.reader(archivo_csv)

    
    # Salta la linea del encabezado si existe y si no hay mas lineas, no genera un error con None
    next(lector, None)
    
    for fila in lector: #recorremos sobre cada linea del archivo
        if len(fila) >= 2:  # Asegurar que hay al menos nombre y puntuación
            nombre = fila[0]
            puntuacion = int(fila[1])
            puntuaciones.append((nombre, puntuacion)) #se agrega la tupla a la lista puntuaciones
    
    archivo_csv.close()
    
    # Ordenanamieto de mayor a mneor utilizando bubble sort
    n = len(puntuaciones)

    for i in range(n):
        for j in range(n - 1 - i):
            if puntuaciones[j][1] < puntuaciones[j + 1][1]:
                puntuaciones[j], puntuaciones[j + 1] = puntuaciones[j + 1], puntuaciones[j]

    return puntuaciones[:10]  # solamente muestra el top10

def agregar_puntuacion_csv(nombre, puntuacion, archivo="assets/puntuaciones.csv"):
    """Agrega una nueva puntuación al archivo CSV"""
    # Abrir archivo y lo agrega al final
    archivo_csv = open(archivo, 'a', encoding='utf-8', newline='')
    escritor = csv.writer(archivo_csv)
    
    # Escribir la nueva puntuación
    escritor.writerow([nombre, puntuacion])
    
    archivo_csv.close()

def es_nuevo_record(puntuacion, archivo="assets/puntuaciones.csv"):
    """Verifica si la puntuación es un nuevo récord"""
    puntuaciones = leer_puntuaciones_csv(archivo)
    
    # Si no hay puntuaciones, cualquier puntaje obtenido es récord
    if not puntuaciones:
        return True
    
    # Obtener la puntuación más alta
    mejor_puntuacion = puntuaciones[0][1]
    
    # Verificamos si la puntuacion obtenida es mayor
    return puntuacion > mejor_puntuacion

def obtener_nombre_jugador(screen, clock, imagen_fondo):
    """Modal para ingresar el nombre del jugador con mayor puntuacion obtenida"""
    font_titulo = pygame.font.Font(None, 40)
    font_texto = pygame.font.Font(None, 36)
    font_instruccion = pygame.font.Font(None, 24)
        
    nombre = ""
    cursor_visible = True
    contador_cursor = 0

    # Carga ed la imagen Record
    imagen_record = pygame.image.load("assets/images/fondos/record.png")
    imagen_record = pygame.transform.scale(imagen_record, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    juego_activo = 1
    while juego_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "JUGADOR"  # Nombre por defecto
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(nombre.strip()) > 0:
                        return nombre.strip()
                    else:
                        return "JUGADOR"  # Nombre por defecto si está vacío
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return "JUGADOR"  # Nombre por defecto si cancela
                else:
                    # Agregar carácter si es alfanumérico y no excede 10 caracteres
                    if len(nombre) < 10 and (event.unicode.isalnum() or event.unicode == " "):
                        nombre += event.unicode.upper()
        
        # Parpadeo del cursor
        contador_cursor += 1
        if contador_cursor > 30:
            cursor_visible = not cursor_visible
            contador_cursor = 0
        
        # Dibujar fondo
        screen.blit(imagen_record, (0, 0))
        
        # Capa semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Contenedor del modal
        modal_ancho = 500
        modal_alto = 250
        modal_x = (SCREEN_WIDTH - modal_ancho) // 2
        modal_y = (SCREEN_HEIGHT - modal_alto) // 2
        
        
        # Modal casi transparente
        modal_surface = pygame.Surface((modal_ancho, modal_alto))
        modal_surface.set_alpha(50)  
        modal_surface.fill((20, 20, 20))
        screen.blit(modal_surface, (modal_x, modal_y))
        
        pygame.draw.rect(screen, COLOR_AMARILLO, (modal_x, modal_y, modal_ancho, modal_alto), 3)


        # Título
        titulo = font_titulo.render("¡NUEVO RECORD ESPACIAL!", True, COLOR_AMARILLO)
        titulo_x = modal_x + (modal_ancho - titulo.get_width()) // 2
        screen.blit(titulo, (titulo_x, modal_y + 20))
        
        # Instrucción
        instruccion = font_instruccion.render("Ingresa tu nombre:", True, COLOR_BLANCO)
        instr_x = modal_x + (modal_ancho - instruccion.get_width()) // 2
        screen.blit(instruccion, (instr_x, modal_y + 60))
        
        # Campo de texto
        texto_nombre = nombre
        if cursor_visible:
            texto_nombre += "_"
        
        nombre_render = font_texto.render(texto_nombre, True, COLOR_VERDE)
        nombre_x = modal_x + (modal_ancho - nombre_render.get_width()) // 2
        screen.blit(nombre_render, (nombre_x, modal_y + 100))
        
        # Instrucciones
        instrucciones = font_instruccion.render("ENTER - Confirmar | ESC - Cancelar", True, COLOR_VERDE)
        instr2_x = modal_x + (modal_ancho - instrucciones.get_width()) // 2
        screen.blit(instrucciones, (instr2_x, modal_y + 150))
        
        pygame.display.flip()
        clock.tick(60)

def mostrar_modal_puntuaciones(screen, clock, imagen_fondo):
    
    """Modal de puntuaciones - no detiene la música"""
    font_titulo = pygame.font.Font(None, 56)
    font_puntuacion = pygame.font.Font(None, 36)
    font_instruccion = pygame.font.Font(None, 28)
    
    
    # Aca secargan las puntuaciones
    puntuaciones = leer_puntuaciones_csv()
    
    juego_activo = 1

    while juego_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "VOLVER" 
        
        # Dibujar fondo
        screen.blit(imagen_fondo, (0, 0))
        
        # Capa semi-transparente para efecto modal
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Contenedor del modal
        modal_ancho = 500
        modal_alto = 400
        modal_x = (SCREEN_WIDTH - modal_ancho) // 2
        modal_y = (SCREEN_HEIGHT - modal_alto) // 2
        
        pygame.draw.rect(screen, (20, 20, 20), (modal_x, modal_y, modal_ancho, modal_alto))
        pygame.draw.rect(screen, COLOR_AMARILLO, (modal_x, modal_y, modal_ancho, modal_alto), 3)
        
        # Título
        titulo = font_titulo.render("TOP 5 PUNTUACIONES", True, COLOR_AMARILLO)
        titulo_x = modal_x + (modal_ancho - titulo.get_width()) // 2
        screen.blit(titulo, (titulo_x, modal_y + 20))
        
        # Línea separadora
        pygame.draw.line(screen, COLOR_GRIS, 
                        (modal_x + 20, modal_y + 70), 
                        (modal_x + modal_ancho - 20, modal_y + 70), 2)
        
        # Mostrar puntuaciones
        y_start = modal_y + 90
        if not puntuaciones:
            # Si no hay puntuaciones
            texto_vacio = font_puntuacion.render("No hay puntuaciones registradas", True, COLOR_GRIS)
            texto_x = modal_x + (modal_ancho - texto_vacio.get_width()) // 2
            screen.blit(texto_vacio, (texto_x, y_start + 50))
        else:
            for i, (nombre, puntuacion) in enumerate(puntuaciones):
                if i < 5:  # Mostrar máximo 5 puntuaciones
                    # Número de posición
                    posicion = font_puntuacion.render(f"{i+1}.", True, COLOR_AMARILLO)
                    
                    # Nombre del jugador
                    nombre_texto = font_puntuacion.render(nombre, True, COLOR_BLANCO)
                    
                    # Puntuación
                    puntuacion_texto = font_puntuacion.render(str(puntuacion), True, COLOR_VERDE)
                    
                    y_pos = y_start + i * 35
                    
                    # Dibujar posición, nombre y puntuación
                    screen.blit(posicion, (modal_x + 30, y_pos))
                    screen.blit(nombre_texto, (modal_x + 70, y_pos))
                    screen.blit(puntuacion_texto, (modal_x + modal_ancho - 120, y_pos))
        
        # Instrucción para salir
        instruccion = font_instruccion.render("ESC - Volver al menu anterior", True, COLOR_VERDE)
        instr_x = modal_x + (modal_ancho - instruccion.get_width()) // 2
        screen.blit(instruccion, (instr_x, modal_y + modal_alto - 40))
        
        pygame.display.flip()
        clock.tick(FPS)

def mostrar_modal_creditos(screen, clock, imagen_fondo):
    """Modal de créditos - no detiene la música"""
    font_titulo = pygame.font.Font(None, 56)
    font_mensaje = pygame.font.Font(None, 28)
    font_instruccion = pygame.font.Font(None, 24)
    mensaje = "Juego desarrollado por La Triada Salvaje:\nAgos, León y Vish\nProfesores: Enzo Zotti y Lucas Ferrini\nUTNFRA 2025\n\nGracias a todos los que jugaron y apoyaron nuestro proyecto.\nEsperamos que lo hayan disfrutado tanto como nosotros al crearlo.\n¡Hasta la próxima aventura!"
        
        
    juego_activo = 1

    while juego_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "VOLVER"
        
        # Dibujar fondo
        screen.blit(imagen_fondo, (0, 0))
        
        # Capa semi-transparente para efecto modal
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Contenedor del modal
        modal_ancho = 700
        modal_alto = 400
        modal_x = (SCREEN_WIDTH - modal_ancho) // 2
        modal_y = (SCREEN_HEIGHT - modal_alto) // 2
        
        pygame.draw.rect(screen, (20, 20, 20), (modal_x, modal_y, modal_ancho, modal_alto))
        pygame.draw.rect(screen, COLOR_AMARILLO, (modal_x, modal_y, modal_ancho, modal_alto), 3)
        
        # Título
        titulo = font_titulo.render("CRÉDITOS", True, COLOR_AMARILLO)
        titulo_x = modal_x + (modal_ancho - titulo.get_width()) // 2
        screen.blit(titulo, (titulo_x, modal_y + 20))
        
        # Línea separadora
        pygame.draw.line(screen, COLOR_GRIS, 
                        (modal_x + 20, modal_y + 70), 
                        (modal_x + modal_ancho - 20, modal_y + 70), 2)
        
        # Se muestra el mensaje de créditos
        y_start = modal_y + 90
        lineas = mensaje.split('\n')
        for i in range(len(lineas)):
            texto_creditos = font_mensaje.render(lineas[i], True, COLOR_BLANCO)
            texto_x = modal_x + (modal_ancho - texto_creditos.get_width()) // 2
            screen.blit(texto_creditos, (texto_x, y_start + i * 30))

        # Instrucciones para salir
        instruccion = font_instruccion.render("ESC - Volver al menu anterior", True, COLOR_VERDE)
        instr_x = modal_x + (modal_ancho - instruccion.get_width()) // 2
        screen.blit(instruccion, (instr_x, modal_y + modal_alto - 40))
        
        pygame.display.flip()
        clock.tick(FPS)

# Funciones para la creacion y caida de enemigos y power ups 

def crear_objetos (crear_funcion, cantidad:int) -> list :
    """
    Genera una lista (en este caso la usamos para enemigos y power ups)
    """    
    lista = []
    for i in range(cantidad):
        lista.append(crear_funcion())
    return lista

def caer_objeto(objeto: dict):
    """
    Se le pasa un diccionario, lo modifica y actualiza, de acuerdo al estado, tiempo y velocidad de aparicion
    """
    if objeto["tiempo_espera"] > 0:
        objeto["tiempo_espera"] -= 1

    if objeto["activo"]:
        objeto["y"] += objeto["velocidad_y"]
        
        # Reiniciar para que vuelva a caer
        if objeto["y"] > SCREEN_HEIGHT:
            objeto["x"] = random.randint(0, SCREEN_WIDTH - 85)
            objeto["y"] = random.randint(-500, -50)
            objeto["velocidad_y"] = random.randint(3, 5)  
            objeto["tiempo_espera"] = random.randint(60, 3600)
            objeto["activo"] = False