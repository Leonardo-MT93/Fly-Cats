# Archivo de configuraciones a cargo de Agos! 
import pygame

def crear_jugador(x, y):
    jugador = {}
    jugador['image'] = pygame.image.load("assets/images/player/gato.png").convert_alpha()
    jugador['rect'] = jugador['image'].get_rect()
    jugador['rect'].topleft = (x, y)
    jugador['speed'] = 5
    return jugador

def mover_jugador(jugador, keys):
    if keys[pygame.K_LEFT]:
        jugador['rect'].x -= jugador['speed']
    if keys[pygame.K_RIGHT]:
        jugador['rect'].x += jugador['speed']

def dibujar_jugador(screen, jugador):
    screen.blit(jugador['image'], jugador['rect'])