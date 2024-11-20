import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tabla de Ruleta de Casino")

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

# Función para dibujar el tablero
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
        y = 50 + row * CELL_HEIGHT

        # Dibujar la celda
        pygame.draw.rect(screen, color, (x, y, CELL_WIDTH, CELL_HEIGHT))
        pygame.draw.rect(screen, WHITE, (x, y, CELL_WIDTH, CELL_HEIGHT), 2)  # Borde blanco

        # Dibujar el número dentro de la celda
        text = font.render(number, True, WHITE if color != BLACK else WHITE)
        screen.blit(text, (x + (CELL_WIDTH - text.get_width()) // 2, y + (CELL_HEIGHT - text.get_height()) // 2))

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Dibujar el fondo
    screen.fill(BROWN)
    
    # Dibujar la tabla de ruleta
    draw_table()
    
    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
