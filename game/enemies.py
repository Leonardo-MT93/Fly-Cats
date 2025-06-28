# Archivo de configuraciones a cargo de Vish! 

# Enemigos: Perro robot

from game.game_manager import pantalla_juego
import pygame
import random
import config

pygame.init()
pygame.image.load()
pygame.time.Clock().tick(30)

imagen_enemigo1 = pygame.image.load("assets/images/enemies/PerroRobot1.png")

velocidad = 3

vuela_enemigo = True
while vuela_enemigo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            vuela_enemigo = False
    pygame.draw.rect(imagen_enemigo1)
    pantalla_juego.blit("assets/images/FondoJuego.png")
    imagen_enemigo1.x += velocidad 

    pygame.display.flip()        


      

pygame.quit()