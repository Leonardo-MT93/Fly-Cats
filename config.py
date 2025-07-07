# Archivo de configuraciones a cargo de León! 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colores del jeugo
COLOR_VERDE = (0, 255, 0)
COLOR_BLANCO = (255, 255, 255)
COLOR_AMARILLO = (255, 255, 0)
COLOR_GRIS = (180, 180, 180)
COLOR_FONDO = (0, 0, 0)

# Rutas de las imagenes
RUTA_IMAGEN_FONDO_MENU_PRINCIPAL = "assets/images/fondos/portada.png"
RUTA_IMAGEN_FIN_DEL_JUEGO = "assets/images/fondos/game_over.png"
RUTA_IMAGEN_PANTALLA_JUEGO = "assets/images/fondos/pantalla_juego.png"
RUTA_IMAGEN_NUEVO_RECORD = "assets/images/fondos/record.png"
RUTA_ICONO_JUEGO = "assets/images/icono.png"
RUTA_IMAGEN_INTRO_1 = "assets/images/intro/intro01.png"
RUTA_IMAGEN_INTRO_2 = "assets/images/intro/intro02.png" 
RUTA_IMAGEN_INTRO_3 = "assets/images/intro/intro03.png"
RUTA_IMAGEN_INTRO_4 = "assets/images/intro/intro04.png"


DURACION_INTRO = 5000  

#Musica
RUTA_MUSICA_MENU = "assets/sounds/music/menu_music.ogg"
RUTA_MUSICA_GAME_OVER = "assets/sounds/music/game_over_music.ogg"
RUTA_MUSICA_GAME = "assets/sounds/music/game_music.ogg"
RUTA_MUSICA_INTRO = "assets/sounds/music/musica_intro.ogg"
RUTA_MUSICA_RECORD = "assets/sounds/music/record_music.ogg"
VOLUMEN_MENU = 0.1
VOLUMEN_GAME_OVER = 0.1
VOLUMEN_MUSICA_INTRO = 0.3
VOLUMEN_MUSICA_RECORD = 0.1

#Sonidos
RUTA_SONIDO_DISPARO = "assets/sounds/effects/disparo.ogg"
VOLUMEN_SONIDO_DISPARO = 0.1
RUTA_SONIDO_MAULLIDO_GATO = "assets/sounds/effects/maullido-gato.ogg"
VOLUMEN_SONIDO_MAULLIDO_GATO = 0.4
RUTA_SONIDO_MUERTE_PERRO = "assets/sounds/effects/golpe-perro.ogg"
VOLUMEN_SONIDO_MUERTE_PERRO = 0.1
RUTA_SONIDA_POWER_UP = "assets/sounds/effects/Power-up.ogg"
VOLUMEN_SONIDO_POWER_UP = 0.4

#Puntuaciones
RUTA_CSV_PUNTUACIONES = "assets/puntuaciones.csv"

#Config del juego
TITULO_JUEGO = "Fly Cats"

#Opciones de menus
OPCIONES_MENU_PRINCIPAL = ["JUGAR", "RANKING", "CREDITOS", "SALIR"]
OPCIONES_GAME_OVER = ["REINTENTAR", "RANKING", "SALIR"]
OPCIONES_RECORD = ["JUGAR OTRA VEZ", "RANKING", "SALIR"]

#estados del juego
ESTADO_INTRO = "INTRO"
ESTADO_MENU = "MENU"
ESTADO_JUEGO = "JUEGO"
ESTADO_GAME_OVER = "GAME_OVER"
ESTADO_NUEVO_RECORD = "NUEVO_RECORD"
