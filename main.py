import pygame
import random
import math
from pygame import mixer

# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo.jpg')

# agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# variables del Jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(1.5)
    enemigo_y_cambio.append(40)

# variables de la bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 5
bala_visible = False

# puntaje
puntaje = 0
fuente = pygame.font.Font(None, 32)
texto_x = 10
texto_y = 10

# texto final de juego
fuente_final = pygame.font.Font(None, 64)


def texto_final():
    mensaje = fuente_final.render("¡GAME OVER!", True, (255, 255, 255))
    puntaje_final = fuente_final.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(mensaje, (200, 200))
    pantalla.blit(puntaje_final, (250, 300))


# funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# fucion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# fucion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
reloj = pygame.time.Clock()

while se_ejecuta:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -5
            elif evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 5
            elif evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    pantalla.blit(fondo, (0, 0))

    jugador_x += jugador_x_cambio

    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    for e in range(cantidad_enemigos):
        enemigo(enemigo_x[e], enemigo_y[e], e)

        # Verificar colisión antes de actualizar la posición
        colision = hay_colision(enemigo_x[e], enemigo_y[e], jugador_x, jugador_y)
        if colision:
            texto_final()
            se_ejecuta = False

        colision_bala = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision_bala:
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)
            bala_visible = False
            bala_y = 500

        enemigo_x[e] += enemigo_x_cambio[e]
        if enemigo_x[e] <= 0 or enemigo_x[e] >= 736:
            enemigo_x_cambio[e] *= -1
            enemigo_y[e] += enemigo_y_cambio[e]

    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    pygame.display.update()

    reloj.tick(60)

# Liberar recursos al salir del juego
mixer.music.stop()
pygame.quit()
