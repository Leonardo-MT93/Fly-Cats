# Archivo de configuraciones a cargo de Agos! 
import pygame
import config
def crear_jugador(screen_width, screen_height) -> tuple:
    """
    Crea y devuelve el jugador con su imagen, posición y velocidad inicial.

    """

    imagen = pygame.image.load("assets/images/player/gato.png").convert_alpha()
    imagen = pygame.transform.scale(imagen, (85, 85))
    rect = imagen.get_rect()
    rect.centerx = screen_width // 2
    rect.bottom = screen_height - 10
    velocidad = 8
    return imagen, rect, velocidad

def mover_jugador(rect, keys, ancho_pantalla, alto_pantalla, velocidad):
    """
    Mueve el rectángulo del jugador basado en las teclas de dirección presionadas
    y mantiene al jugador dentro de los límites de la pantalla.

    """

    if keys[pygame.K_LEFT]:
        rect.x -= velocidad
    if keys[pygame.K_RIGHT]:
        rect.x += velocidad
    if keys[pygame.K_UP]:
        rect.y -= velocidad
    if keys[pygame.K_DOWN]:
        rect.y += velocidad

    # Limitar dentro de los bordes de la pantalla
    if rect.left < 0:
        rect.left = 0
    if rect.right > ancho_pantalla:
        rect.right = ancho_pantalla
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > alto_pantalla:
        rect.bottom = alto_pantalla

def dibujar_jugador(screen, imagen, rect):
    """
    Dibuja el jugador en la pantalla en la posición especificada por el rectángulo.

    """

    screen.blit(imagen, rect)