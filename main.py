import pygame
import sys
from config import *

def cargar_imagen_fondo(ruta_imagen):
    imagen = pygame.image.load(ruta_imagen)
    # Escalar la imagen al tamaño de la pantalla
    imagen_escalada = pygame.transform.scale(imagen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return imagen_escalada
def dibujar_menu(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo):
    """Dibuja todo el menú en pantalla"""
    # Fuentes
    font_titulo = pygame.font.Font(None, 72)
    font_botones = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    # Colores
    color_verde = (0, 255, 0)
    color_blanco = (255, 255, 255)
    color_amarillo = (255, 255, 0)
    color_fondo = (0, 0, 0)
    # imagen_de_fondo = pygame.image.load("assets/images/portada.png")

    # Dibujar fondo
    if imagen_fondo:
        # Fondo negro primero
        screen.fill(color_fondo)
        # Centrar la imagen
        x = (SCREEN_WIDTH - imagen_fondo.get_width()) // 2
        y = (SCREEN_HEIGHT - imagen_fondo.get_height()) // 2
        screen.blit(imagen_fondo, (x, y))
    else:
        # Fondo negro si no hay imagen
        screen.fill(color_fondo)
    
    # Opciones del menú
    y_start = 350
    for i, opcion in enumerate(opciones):
        # Color de la opción
        if i == opcion_seleccionada:
            # Efecto de parpadeo para la opción seleccionada
            if contador_parpadeo % 30 < 15:
                color = color_amarillo
            else:
                color = color_blanco
        else:
            color = color_blanco
        
        # Renderizar texto
        texto = font_botones.render(opcion, True, color)
        x = SCREEN_WIDTH // 2 - texto.get_width() // 2
        y = y_start + i * 60
        
        # Indicador de selección
        if i == opcion_seleccionada:
            indicador = font_botones.render(">", True, color_amarillo)
            screen.blit(indicador, (x - 50, y))
        
        screen.blit(texto, (x, y))
    
    # Instrucciones
    instruccion = font_small.render("Usa UP | DOWN para navegar, ENTER para seleccionar", 
                                   True, color_verde)
    instr_x = SCREEN_WIDTH // 2 - instruccion.get_width() // 2
    screen.blit(instruccion, (instr_x, SCREEN_HEIGHT - 50))

def mostrar_menu(screen, clock):

    opciones = ["JUGAR", "PUNTUACIONES", "SALIR"]
    opcion_seleccionada = 0
    contador_parpadeo = 0

    imagen_fondo = cargar_imagen_fondo("assets/images/portada.png")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return opciones[opcion_seleccionada]
        
        contador_parpadeo += 1
        dibujar_menu(screen, opciones, opcion_seleccionada, contador_parpadeo, imagen_fondo)
        
        pygame.display.flip()
        clock.tick(60)

def juego_principal(screen, clock):
    
    superficie_secundaria = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    superficie_secundaria.fill((0,0,0))
   
    player_x = 400
    player_y = 300
    player_size = 38
    player_speed = 5
   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"  # Volver al menú
       
        # Comandos direccionales
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed
       
        # Dibujar todo
        screen.fill((128, 0, 128))
        screen.blit(superficie_secundaria, (50, 50))
        pygame.draw.circle(screen, (255, 255, 255), 
                         (player_x + player_size//2, player_y + player_size//2), 
                         player_size//2)
       
        pygame.display.flip()
        clock.tick(FPS)

def main():
    """Función principal que maneja menú y juego"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    corriendo_juego = True
    while corriendo_juego:
        # Mostrar menú y obtener opción
        opcion = mostrar_menu(screen, clock)
        
        if opcion == "JUGAR":
            resultado = juego_principal(screen, clock)
            if resultado == "SALIR":
                break
            # Si resultado == "MENU", vuelve al while y muestra el menú
            
        elif opcion == "PUNTUACIONES":
            # Aquí podrías agregar una función mostrar_puntuaciones()
            print("Mostrar puntuaciones...")
            
        elif opcion == "OPCIONES":
            # Aquí podrías agregar una función mostrar_opciones()
            print("Mostrar opciones...")
            
        elif opcion == "SALIR":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()