import pygame
import sys
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruleta de Casino con Tabla")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BROWN = (215, 129, 36)

# Fuente
font = pygame.font.SysFont("Arial", 24)

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

# Crear una instancia de la ruleta
ruleta = Ruleta()

# Función para dibujar la tabla de ruleta
def draw_table():
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

# Bucle principal del juego
running = True
winning_number = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Presiona espacio para girar la ruleta
                winning_number, _ = ruleta.girar()

    # Dibujar el fondo
    screen.fill(BROWN)
    
    # Dibujar la tabla de ruleta
    draw_table()
    
    # Dibujar la ruleta circular con colores correspondientes
    draw_roulette(winning_number)
    
    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
