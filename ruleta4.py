#!/usr/bin/env python3
import pygame
import sys
import random
import math

# Configuració del joc
WIDTH, HEIGHT = 1200, 700
FPS = 60
NUMEROS = list(range(37))
COLORS = {0: (0, 255, 0), **{n: (255, 0, 0) if n % 2 else (0, 0, 0) for n in range(1, 37)}}

# Inicialitzar Pygame
pygame.init()
random.seed(None)  # Reinicia el generador aleatori
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruleta de Casino")
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

# Colors
BROWN = (139, 69, 19)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Classe per a la ruleta
class Ruleta:
    def __init__(self):
        self.resultat = None

    def girar(self):
        """Seleccionar un número aleatori com a resultat."""
        self.resultat = random.choice(NUMEROS)
        return self.resultat

# Classe jugador
class Jugador:
    def __init__(self, nom, saldo=100):
        self.nom = nom
        self.saldo = saldo
        self.apostes = []  # (tipus, quantitat, valor)

    def apostar(self, tipus, quantitat, valor):
        if quantitat > self.saldo:
            raise ValueError(f"{self.nom} no té saldo suficient.")
        self.saldo -= quantitat
        self.apostes.append((tipus, quantitat, valor))

    def afegir_guanys(self, quantitat):
        self.saldo += quantitat

# Funció per dibuixar la ruleta circular
def dibuixar_ruleta(winning_number=None, angle=0):
    """Dibuixa la ruleta amb un indicador del número guanyador."""
    center = (600, 300)
    radius = 200
    num_sectors = len(NUMEROS)
    angle_per_sector = 360 / num_sectors

    # Dibuixar sectors
    for i, num in enumerate(NUMEROS):
        start_angle = math.radians(i * angle_per_sector + angle)
        end_angle = math.radians((i + 1) * angle_per_sector + angle)
        color = COLORS[num]

        points = [center]
        for angle_deg in range(int(start_angle * 180 / math.pi), int(end_angle * 180 / math.pi) + 1):
            x = center[0] + radius * math.cos(math.radians(angle_deg))
            y = center[1] - radius * math.sin(math.radians(angle_deg))
            points.append((x, y))
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 1)

    # Dibuixar els números
    for i, num in enumerate(NUMEROS):
        num_angle = math.radians(i * angle_per_sector + angle_per_sector / 2 + angle)
        x = center[0] + (radius - 30) * math.cos(num_angle)
        y = center[1] - (radius - 30) * math.sin(num_angle)
        text = font.render(str(num), True, WHITE if COLORS[num] != BLACK else RED)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    # Dibuixar fletxa indicador
    pygame.draw.line(screen, RED, (center[0], center[1] - radius - 20), (center[0], center[1] - radius + 20), 5)

# Funció per dibuixar la taula rectangular de la ruleta
def dibuixar_taula():
    """Dibuixa una taula rectangular amb els números de la ruleta."""
    CELL_WIDTH = 80
    CELL_HEIGHT = 50
    for i, num in enumerate(NUMEROS):
        row = (i - 1) // 3 if num != 0 else 0
        col = (i - 1) % 3 if num != 0 else 0
        x = 50 + col * CELL_WIDTH if num != 0 else 0
        y = 50 + row * CELL_HEIGHT if num != 0 else 0

        color = COLORS[num]
        pygame.draw.rect(screen, color, (x, y, CELL_WIDTH, CELL_HEIGHT))
        pygame.draw.rect(screen, WHITE, (x, y, CELL_WIDTH, CELL_HEIGHT), 2)

        text = font.render(str(num), True, WHITE if color != BLACK else RED)
        screen.blit(text, (x + (CELL_WIDTH - text.get_width()) // 2, y + (CELL_HEIGHT - text.get_height()) // 2))

# Simulació de l'animació de gir
def animar_gir(ruleta, girs=10):
    """Simula el gir de la ruleta amb velocitat decreixent."""
    angle = 0
    velocitat = 20  # Velocitat inicial en graus/frame
    while velocitat > 0:
        screen.fill(BROWN)
        dibuixar_taula()
        angle += velocitat
        dibuixar_ruleta(angle=angle % 360)
        pygame.display.flip()
        clock.tick(FPS)
        velocitat -= 0.5  # Reduir velocitat progressivament
    return ruleta.girar()

# Bucle principal del joc
ruleta = Ruleta()
jugadors = [Jugador("Taronja"), Jugador("Lila"), Jugador("Blau")]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Botó de girar
            x, y = pygame.mouse.get_pos()
            if 800 <= x <= 900 and 500 <= y <= 550:  # Botó "Girar"
                numero_guanyador = animar_gir(ruleta)

    # Dibuixar la pantalla
    screen.fill(BROWN)
    dibuixar_taula()
    dibuixar_ruleta()
    pygame.draw.rect(screen, RED, (800, 500, 100, 50))
    screen.blit(font.render("GIRAR", True, WHITE), (820, 510))
    pygame.display.flip()

pygame.quit()
sys.exit()
