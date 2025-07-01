# Archivo de configuraciones a cargo de Agos! 
import pygame
import config
def crear_jugador(screen_width, screen_height):
    jugador = {}
    imagen_original = pygame.image.load("assets/images/player/gato.png").convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen_original, (85, 85))  
    jugador['image'] = imagen_escalada
    jugador['rect'] = jugador['image'].get_rect()
    
    # Centrado horizontal y parte inferior de la pantalla
    jugador['rect'].centerx = screen_width // 2
    jugador['rect'].bottom = screen_height - 10
    
    jugador['speed'] = 5
    return jugador

def mover_jugador(jugador, keys, ancho_pantalla, alto_pantalla):
    if keys[pygame.K_LEFT]:
        jugador['rect'].x -= jugador['speed']
    if keys[pygame.K_RIGHT]:
        jugador['rect'].x += jugador['speed']
    if keys[pygame.K_UP]:
        jugador['rect'].y -= jugador['speed']
    if keys[pygame.K_DOWN]:
        jugador['rect'].y += jugador['speed']

    # Limitar dentro de los bordes de la pantalla
    if jugador['rect'].left < 0:
        jugador['rect'].left = 0
    if jugador['rect'].right > ancho_pantalla:
        jugador['rect'].right = ancho_pantalla
    if jugador['rect'].top < 0:
        jugador['rect'].top = 0
    if jugador['rect'].bottom > alto_pantalla:
        jugador['rect'].bottom = alto_pantalla

def dibujar_jugador(screen, jugador):
    screen.blit(jugador['image'], jugador['rect'])