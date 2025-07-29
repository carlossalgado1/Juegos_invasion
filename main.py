import pygame
import random
import math

# Inicialización
pygame.init()

# Pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasión Espacial")
pygame.display.set_icon(pygame.image.load("imagenes/ovni.png"))

# Fondo con imagen
fondo = pygame.transform.scale(pygame.image.load("imagenes/espacio.jpg"), (800, 600))

# Fuente
fuente = pygame.font.Font(None, 48)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Estados del juego
EN_JUEGO = False
JUEGO_TERMINADO = False
JUEGO_GANADO = False

# Jugador
img_jugador = pygame.image.load("imagenes/astronave.png")
jugador_x = 370
jugador_y = 520
jugador_x_cambio = 0
velocidad_jugador = 3

# Enemigos
img_enemigo = pygame.image.load("imagenes/nave-espacial.png")
num_enemigos = 6
enemigos = []

def crear_enemigos():
    enemigos.clear()
    for _ in range(num_enemigos):
        enemigos.append({
            'x': random.randint(0, 736),
            'y': random.randint(50, 150),
            'cambio_x': 2,
            'cambio_y': 40
        })

crear_enemigos()

# Bala
img_bala = pygame.image.load("imagenes/bala.png")
bala_x = 0
bala_y = jugador_y
bala_y_cambio = 4
bala_estado = "listo"

# Funciones
def dibujar_jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def dibujar_enemigo(x, y):
    pantalla.blit(img_enemigo, (x, y))

def disparar_bala(x, y):
    global bala_estado
    bala_estado = "disparo"
    pantalla.blit(img_bala, (x + 20, y))

def colision(obj1_x, obj1_y, obj2_x, obj2_y, distancia=27):
    return math.hypot(obj1_x - obj2_x, obj1_y - obj2_y) < distancia

def mostrar_texto(texto, x, y, color=BLANCO, size=48):
    fuente_local = pygame.font.Font(None, size)
    render = fuente_local.render(texto, True, color)
    pantalla.blit(render, (x, y))

def pantalla_inicio():
    pantalla.blit(fondo, (0, 0))
    mostrar_texto("Invasión Espacial", 240, 200)
    mostrar_texto("Presiona ESPACIO para comenzar", 180, 300)
    pygame.display.update()

def pantalla_game_over():
    pantalla.blit(fondo, (0, 0))
    mostrar_texto("¡GAME OVER!", 280, 250, ROJO)
    mostrar_texto("Presiona R para reiniciar", 210, 320)
    pygame.display.update()

def pantalla_victoria():
    pantalla.blit(fondo, (0, 0))
    mostrar_texto("¡GANASTE!", 300, 250, (0, 255, 0))
    mostrar_texto("Presiona R para jugar de nuevo", 170, 320)
    pygame.display.update()

# Game loop
clock = pygame.time.Clock()
se_ejecuta = True

while se_ejecuta:
    if not EN_JUEGO and not JUEGO_TERMINADO and not JUEGO_GANADO:
        pantalla_inicio()

    if JUEGO_TERMINADO:
        pantalla_game_over()

    if JUEGO_GANADO:
        pantalla_victoria()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if not EN_JUEGO and evento.key == pygame.K_SPACE:
                EN_JUEGO = True
                JUEGO_TERMINADO = False
                JUEGO_GANADO = False

            if EN_JUEGO:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = -velocidad_jugador
                if evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = velocidad_jugador
                if evento.key == pygame.K_SPACE and bala_estado == "listo":
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

            if (JUEGO_TERMINADO or JUEGO_GANADO) and evento.key == pygame.K_r:
                jugador_x = 370
                bala_y = jugador_y
                bala_estado = "listo"
                crear_enemigos()
                EN_JUEGO = True
                JUEGO_TERMINADO = False
                JUEGO_GANADO = False

        if evento.type == pygame.KEYUP:
            if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                jugador_x_cambio = 0

    if EN_JUEGO:
        pantalla.blit(fondo, (0, 0))

        # Movimiento del jugador
        jugador_x += jugador_x_cambio
        jugador_x = max(0, min(jugador_x, 736))
        dibujar_jugador(jugador_x, jugador_y)

        # Movimiento de la bala
        if bala_estado == "disparo":
            disparar_bala(bala_x, bala_y)
            bala_y -= bala_y_cambio
            if bala_y < 0:
                bala_y = jugador_y
                bala_estado = "listo"

        # Enemigos
        for enemigo in enemigos[:]:  # Copia para poder eliminar durante el bucle
            enemigo['x'] += enemigo['cambio_x']
            if enemigo['x'] <= 0 or enemigo['x'] >= 736:
                enemigo['cambio_x'] *= -1
                enemigo['y'] += enemigo['cambio_y']

            # Colisión con jugador
            if colision(jugador_x, jugador_y, enemigo['x'], enemigo['y'], 40):
                EN_JUEGO = False
                JUEGO_TERMINADO = True

            # Colisión con bala
            if bala_estado == "disparo" and colision(enemigo['x'], enemigo['y'], bala_x, bala_y):
                bala_y = jugador_y
                bala_estado = "listo"
                enemigos.remove(enemigo)

            dibujar_enemigo(enemigo['x'], enemigo['y'])

        # Condición de victoria
        if len(enemigos) == 0:
            EN_JUEGO = False
            JUEGO_GANADO = True

        pygame.display.update()

    clock.tick(60)
