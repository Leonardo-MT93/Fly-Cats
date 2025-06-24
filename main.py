# Archivo de configuraciones a cargo de León! 
# Configuraciones principales del juego

import pygame
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders - Testeado con un puntito blanco xD")
    clock = pygame.time.Clock()
    
    # Variables del jugador (punto creado)
    player_x = 400  # Posicion central del punto
    player_y = 300
    player_size = 38  # Tamaño del punto que se mueve con las teclas
    player_speed = 5
    
    running = True
    while running:
        # Evento para poder cerrar el juego si tocas la CRUZ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Comandos direccionales para manejar el punto ya creado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed
        
        
        screen.fill((128, 0, 128))  # Color de fondo de la pantalla creada
        pygame.draw.circle(screen, (255, 255, 255), (player_x + player_size//2, player_y + player_size//2), player_size//2)  # Color de l punto que se maneja con los direccionales. Todo en prueba
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()