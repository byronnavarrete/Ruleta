#!/usr/bin/env python3
import pygame
import sys
import random
import math
import pydevd_file_utils
# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruleta de Casino con Tabla")
FPS = 60
# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BROWN = (215, 129, 36)

# Fuente
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

# Configuración de la tabla de ruleta
numbers = [
    ('0', GREEN), ('1', RED), ('2', BLACK), ('3', RED), ('4', BLACK), ('5', RED), ('6', BLACK),
    ('7', RED), ('8', BLACK), ('9', RED), ('10', BLACK), ('11', BLACK), ('12', RED),
    ('13', BLACK), ('14', RED), ('15', BLACK), ('16', RED), ('17', BLACK), ('18', RED),
    ('19', RED), ('20', BLACK), ('21', RED), ('22', BLACK), ('23', RED), ('24', BLACK),
    ('25', RED), ('26', BLACK), ('27', RED), ('28', BLACK), ('29', BLACK), ('30', RED),
    ('31', BLACK), ('32', RED), ('33', BLACK), ('34', RED), ('35', BLACK), ('36', RED)
]

# Tamaño de cada celda en la tabla
CELL_WIDTH = 80
CELL_HEIGHT = 50

# Configuración de la ruleta
NUMEROS = list(range(37))  # De 0 a 36
COLORS = {int(numbers[i][0]): numbers[i][1] for i in range(len(numbers))}

class Ruleta:
    def __init__(self):
        self.resultado = None

    def girar(self):
        self.resultado = random.choice(NUMEROS)
        return self.resultado, COLORS[self.resultado]

class Jugador:
    def __init__(self, nom, saldo=100):
        self.nom = nom
        self.saldo = saldo
        self.fitxes = {100: 0, 50: 1, 20: 1, 10: 2, 5: 2}
        self.apostes = []

    def apostar(self, tipus, quantitat, valor):
        if quantitat > self.saldo:
            raise ValueError(f"{self.nom} no té saldo suficient.")
        self.saldo -= quantitat
        self.apostes.append((tipus, quantitat, valor))

    def mostrar_fitxes(self):
        return f"{self.nom}: Sald: {self.saldo} | Fitxes: {self.fitxes}"

    def afegir_guanys(self, quantitat):
        self.saldo += quantitat

# Crear una instancia de la ruleta
ruleta = Ruleta()


def calcular_guanys(jugador, aposta, resultat):
    tipus, quantitat, valor = aposta
    guany = 0
    if tipus == "numero" and resultat["numero"] == valor:
        guany = quantitat * 35
    elif tipus == "color" and resultat["color"] == valor:
        guany = quantitat * 1
    elif tipus == "parell/senar" and resultat["parell/senar"] == valor:
        guany = quantitat * 1
    elif tipus == "columna" and resultat["columna"] == valor:
        guany = quantitat * 2
    return guany

def processar_apostes(jugadors, resultat):
    banca = 0
    for jugador in jugadors:
        guany_total = 0
        for aposta in jugador.apostes:
            guany = calcular_guanys(jugador, aposta, resultat)
            if guany > 0:
                guany_total += guany
            else:
                banca += aposta[1]  # Suma les apostes perdudes a la banca
        jugador.guanyar(guany_total)
        jugador.apostes = []  # Esborrar apostes
    return banca

# Función para dibujar la tabla de ruleta
def draw_table():
    
    CELL_WIDTH = 80
    CELL_HEIGHT = 50

    # Coordenades inicials
    OFFSET_X = 100
    OFFSET_Y = 100


    # Dibujar el número 0 en una celda separada
    pygame.draw.rect(screen, GREEN, (50, 50, CELL_WIDTH, CELL_HEIGHT))
    text = font.render('0', True, WHITE)
    screen.blit(text, (50 + (CELL_WIDTH - text.get_width()) // 2, 50 + (CELL_HEIGHT - text.get_height()) // 2))
    
    # Dibujar los números del 1 al 36 en la tabla
    for i, (number, color) in enumerate(numbers[1:], start=1):
        row = (i - 1) // 3
        col = (i - 1) % 3
        x = 150 + col * CELL_WIDTH
        y = 0 + row * CELL_HEIGHT

        # Dibujar la celda
        pygame.draw.rect(screen, color, (x, y, CELL_WIDTH, CELL_HEIGHT))
        pygame.draw.rect(screen, WHITE, (x, y, CELL_WIDTH, CELL_HEIGHT), 2)  # Borde blanco

        # Dibujar el número dentro de la celda
        text = font.render(number, True, WHITE if color != BLACK else WHITE)
        screen.blit(text, (x + (CELL_WIDTH - text.get_width()) // 2, y + (CELL_HEIGHT - text.get_height()) // 2))
    # Espais d'aposta horitzontals a sota de la ruleta
    apuesta_y = OFFSET_Y + 550  # Alçada de la base per les apostes
    espacio_entre = 40

    # Espais per vermell/negre
    pygame.draw.rect(screen, RED, (OFFSET_X, apuesta_y, 550, 200))  # Vermell
    pygame.draw.rect(screen, BLACK, (OFFSET_X, apuesta_y, 550, 200), 2)
    pygame.draw.rect(screen, BLACK, (OFFSET_X + 170, apuesta_y, 550, 200))  # Negre
    screen.blit(font.render("VERMELL", True, WHITE), (OFFSET_X + 20, apuesta_y + 15))
    screen.blit(font.render("NEGRE", True, WHITE), (OFFSET_X + 190, apuesta_y + 15))

    # Espais per parell/senar
    pygame.draw.rect(screen, WHITE, (OFFSET_X + 340, apuesta_y, 350, 200))  # Parell
    pygame.draw.rect(screen, WHITE, (OFFSET_X + 540, apuesta_y, 520, 200))  # Senar
    pygame.draw.rect(screen, BLACK, (OFFSET_X + 340, apuesta_y, 400, 200), 2)
    pygame.draw.rect(screen, BLACK, (OFFSET_X + 492, apuesta_y, 480, 200), 2)
    screen.blit(font.render("PARELL", True, BLACK), (OFFSET_X + 400, apuesta_y + 15))
    screen.blit(font.render("SENAR", True, BLACK), (OFFSET_X + 500, apuesta_y + 15))

    # Espais per les tres columnes
    for i in range(3):
        x = OFFSET_X + 680 + i * (150 + espacio_entre)
        pygame.draw.rect(screen, GREEN, (x, apuesta_y, 750, 200))
        pygame.draw.rect(screen, BLACK, (x, apuesta_y, 750, 200), 2)
        screen.blit(font.render(f"COLUMNA {i+1}", True, BLACK), (x + 20, apuesta_y + 15))

    # Quadre de "Banca" a la dreta
    pygame.draw.rect(screen, BROWN, (1000, 500, 200, 80))  # Banca
    pygame.draw.rect(screen, WHITE, (1000, 500, 200, 80), 2)  # Contorn
    screen.blit(font.render("BANCA", True, WHITE), (1050, 530))

    # quadre de "gira"
    pygame.draw.rect(screen, BROWN, (600, 500, 200, 60))  # Dibujar rectángulo
    pygame.draw.rect(screen, RED, (600, 500, 200, 60), 4)  # Borde del botón
    text = font.render("GIRAR", True, WHITE)
    screen.blit(text, (650, 520))  # Posicionar texto en el botón

# Función para dibujar la ruleta circular con colores correspondientes
def draw_roulette(winning_number=None):
    center = (900, 300)
    radius = 200
    num_sectors = len(NUMEROS)
    angle_per_sector = 360 / num_sectors

    # Dibujar los sectores de la ruleta con sus colores
    for i, num in enumerate(NUMEROS):
        start_angle = math.radians(i * angle_per_sector)
        end_angle = math.radians((i + 1) * angle_per_sector)
        color = COLORS[num]
        
        # Dibujar cada sector usando draw.pie (simulado con polígonos)
        points = [center]
        for angle in range(int(start_angle * 180 / math.pi), int(end_angle * 180 / math.pi) + 1):
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] - radius * math.sin(math.radians(angle))
            points.append((x, y))
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 1)  # Borde de cada sector

    # Dibujar los números encima de los sectores
    for i, num in enumerate(NUMEROS):
        angle = math.radians(i * angle_per_sector + angle_per_sector / 2)
        x = center[0] + (radius - 30) * math.cos(angle)
        y = center[1] - (radius - 30) * math.sin(angle)
        text = font.render(str(num), True, WHITE if COLORS[num] != BLACK else WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    
    # Dibujar el número ganador si existe
    if winning_number is not None:
        pygame.draw.circle(screen, RED, center, 15)
        result_text = font.render(f"Resultat: {winning_number}", True, WHITE)
        screen.blit(result_text, (700, 600))
    pygame.draw.line(screen, RED, (center[0], center[1] - radius - 10), (center[0], center[1] - radius - 30), 4)
    
# Simulació de l'animació de gir
def animar_gir(ruleta, girs=15):
    """Simula el gir de la ruleta amb velocitat decreixent."""
    angle = 0
    velocitat = 20  # Velocitat inicial en graus/frame
    while velocitat > 0:
        screen.fill(BROWN)
        draw_table()
        angle += velocitat
        draw_roulette(angle=angle % 360)
        pygame.display.flip()
        clock.tick(FPS)
        velocitat -= 0.5  # Reduir velocitat progressivament
    return ruleta.girar()

# Bucle principal del joc
ruleta = Ruleta()
jugadors = [Jugador("Taronja"), Jugador("Lila"), Jugador("Blau")]


# Actualització del càlcul de resultats i gestió d'apostes
def processar_resultats(jugadors, resultat):
    banca = 0  # Fitxes perdudes que van a la banca
    for jugador in jugadors:
        guany_total = 0
        for tipus, quantitat, valor in jugador.apostes:
            guany = 0
            if tipus == "numero" and resultat["numero"] == valor:
                guany = quantitat * 35
            elif tipus == "color" and resultat["color"] == valor:
                guany = quantitat * 1
            elif tipus == "parell/senar" and resultat["parell/senar"] == valor:
                guany = quantitat * 1
            elif tipus == "columna" and resultat["columna"] == valor:
                guany = quantitat * 2
            
            if guany > 0:
                guany_total += guany
            else:
                banca += quantitat  # Les apostes perdudes van a la banca
        
        jugador.afegir_guanys(guany_total)
        jugador.apostes = []  # Netejar apostes després de processar-les
    return banca


# Comprovar si s'ha acabat el joc
def verificar_final_partida(jugadors):
    return all(jugador.saldo == 0 for jugador in jugadors)


# Funció per animar les fitxes perdudes a la "Banca"
def animar_fitxes_a_banca(banca):
    pygame.draw.rect(screen, BROWN, (1000, 500, 200, 80))  # Quadre de la banca
    text = font.render(f"BANCA: {banca}", True, WHITE)
    screen.blit(text, (1050, 530))


# Bucle principal amb les noves funcionalitats
running = True
winning_number = None
banca = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 700 <= x <= 900 and 500 <= y <= 580:  # Botó "Girar"
                # Resultat de la ruleta
                winning_number, resultat_color = ruleta.girar()
                resultat = {
                    "numero": winning_number,
                    "color": resultat_color,
                    "parell/senar": "parell" if winning_number % 2 == 0 else "senar",
                    "columna": (winning_number - 1) % 3 + 1 if winning_number != 0 else None,
                }

                # Processar resultats de les apostes
                banca = processar_resultats(jugadors, resultat)

                # Comprovar si el joc ha acabat
                if verificar_final_partida(jugadors):
                    print("Fi de la partida! Tots els jugadors s'han arruïnat.")
                    running = False

    # Dibuixar elements gràfics
    screen.fill(BROWN)
    draw_table()
    draw_roulette(winning_number)
    animar_fitxes_a_banca(banca)

    # Actualitzar la pantalla
    pygame.display.flip()

# Sortir del programa
pygame.quit()
sys.exit()
