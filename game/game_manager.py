# Archivo de configuraciones a cargo de León! 
import pygame
import sys

NOMBRE_JUEGO = "Fly Cats"

def mostrar_menu():
    print("Bienvenido a", NOMBRE_JUEGO)
    print("1. Jugar")
    print("2. Puntajes")
    print("3. Salir")
    
    opcion = input("Selecciona una opción: ")
    
    if opcion == "1":
        iniciar_juego()
    elif opcion == "2":
        salir_juego()
    else:
        print("Opción no válida. Inténtalo de nuevo.")
        mostrar_menu()


def iniciar_juego():
    print("Iniciando el juego...")
    # Aquí iría la lógica del juego
    # Por ahora, solo mostramos un mensaje de prueba
    print("¡Juego iniciado! (Lógica del juego aún no implementada)")
    
    # Después de iniciar el juego, podrías volver al menú o salir
    mostrar_menu()

def salir_juego():
    print("Saliendo del juego...")
    # Aquí podrías guardar puntajes o realizar otras acciones antes de salir
    print("¡Gracias por jugar!", NOMBRE_JUEGO)
    exit()

def manejar_input_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir_juego()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    iniciar_juego()
                elif event.key == pygame.K_2:
                    print("Mostrando puntajes... (Funcionalidad aún no implementada)")
                elif event.key == pygame.K_3:
                    salir_juego()
                else:
                    print("Opción no válida. Presiona 1, 2 o 3.")

def menu_principal():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(NOMBRE_JUEGO)
    
    # Lógica del menú principal
    mostrar_menu()
    
    while True:
        manejar_input_menu()
        pygame.display.flip()

def comenzar_juego():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(NOMBRE_JUEGO)
    
    # Aquí podrías iniciar la lógica del juego
    print("¡Juego iniciado! (Lógica del juego aún no implementada)")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir_juego()
        
        screen.fill((0, 0, 0))  # Limpiar pantalla
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(NOMBRE_JUEGO)
    
    # Mostrar el menú principal
    menu_principal()
    
    # Iniciar el juego
    comenzar_juego()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
