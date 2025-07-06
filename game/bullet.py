# Archivo de configuraciones a cargo de Agos! import pygame
import pygame
def crear_bala(x, y) -> tuple:
    """
    Crea una bala en forma de bola de estambre en una posición dada.

    """

    imagen = pygame.image.load("assets/images/Balas/bola-estambre.png").convert_alpha()
    imagen = pygame.transform.scale(imagen, (25, 25))
    rect = imagen.get_rect(center=(x, y))
    velocidad = -8
    return imagen, rect, velocidad

def mover_bala(rect, velocidad):
    """
    Mueve la bala actualizando su posición vertical.
    
    """

    rect.y += velocidad

def dibujar_bala(screen, imagen, rect):
    """
    Dibuja una bala en una pantalla dada en la posición almacenada en su rectangulo.

    """
    screen.blit(imagen, rect)

def bala_fuera_de_pantalla(rect) -> bool:
    """
    Verifica si una bala se encuentra fuera de la pantalla (es decir,
    si se encuentra arriba de la pantalla).

    Parameters
    ----------
    rect : pygame.Rect
        El rectangulo de la bala.

    Returns
    -------
    bool
        True si la bala se encuentra fuera de la pantalla,
        False en caso contrario.
    """
    return rect.bottom < 0