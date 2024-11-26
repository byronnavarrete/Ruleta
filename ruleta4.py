#!/usr/bin/env python3
import pygame
import sys
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1200, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruleta de Casino con Botón Girar")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (28, 84, 45)
WHITE = (255, 255, 255)
BROWN = (215, 129, 36)
GRAY = (200, 200, 200)
DARK_GRAY = (169, 169, 169)
GREEN2 = (0, 128, 0)

# Fuente
font = pygame.font.SysFont("Arial", 24)
button_font = pygame.font.SysFont("Arial", 28)

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
CELL_WIDTH = 70
CELL_HEIGHT = 40
CELL_WIDTH2 = 70
CELL_HEIGHT2 = 160
CELL_WIDTH3 = 80
CELL_HEIGHT3 = 80

# Configuración de la ruleta
NUMEROS = list(range(37))  # De 0 a 36
COLORS = {int(numbers[i][0]): numbers[i][1] for i in range(len(numbers))}
FICHA_VALORES = [5, 10, 20, 50, 100]
JUGADORES = {
    "naranja": (255, 165, 0),
    "lila": (128, 0, 128),
    "azul": (0, 0, 255)
}


class Ruleta:
    def __init__(self):
        self.resultado = None

    def girar(self):
        self.resultado = random.choice(NUMEROS)
        return self.resultado, COLORS[self.resultado]

# Crear una instancia de la ruleta
ruleta = Ruleta()

class Jugador:
    def __init__(self, nombre, color, saldo_inicial=100):
        self.nombre = nombre
        self.color = color
        self.saldo = saldo_inicial
        self.fichas = self._distribuir_fichas(saldo_inicial)

    def _distribuir_fichas(self, saldo):
        # Distribuir fichas para que sumen al saldo inicial
        fichas = {valor: 0 for valor in FICHA_VALORES}
        for valor in sorted(FICHA_VALORES, reverse=True):
            fichas[valor] = saldo // valor
            saldo %= valor
        return fichas

    def reorganizar_fichas(self):
        # Reorganizar fichas para maximizar la variedad
        nuevo_saldo = sum(valor * cantidad for valor, cantidad in self.fichas.items())
        self.fichas = {valor: 0 for valor in FICHA_VALORES}
        for valor in FICHA_VALORES:
            if nuevo_saldo >= valor:
                self.fichas[valor] = 1
                nuevo_saldo -= valor
        self.saldo = sum(valor * cantidad for valor, cantidad in self.fichas.items())


jugadores = [Jugador(nombre, color) for nombre, color in JUGADORES.items()]
# Crear jugadores
def draw_players(jugadores):
    start_x, start_y = 50, 550  # Posición inicial para dibujar
    spacing_y = 150  # Espaciado vertical entre jugadores

    for i, jugador in enumerate(jugadores):
        x, y = start_x, start_y + i * spacing_y

        # Dibujar el nombre del jugador
        name_text = font.render(jugador.nombre.capitalize(), True, jugador.color)
        screen.blit(name_text, (x, y))

        # Dibujar las fichas
        x_offset = 150
        for valor, cantidad in jugador.fichas.items():
            # Dibujar el rectángulo de la ficha
            ficha_rect = pygame.Rect(x + x_offset, y - 20, 50, 40)
            pygame.draw.rect(screen, jugador.color, ficha_rect)
            pygame.draw.rect(screen, WHITE, ficha_rect, 2)

            # Dibujar el valor y cantidad de fichas
            ficha_text = font.render(f"{valor:03d} x{cantidad}", True, WHITE)
            screen.blit(ficha_text, (x + x_offset + 60, y - 10))

            x_offset += 150

        # Dibujar el saldo disponible
        saldo_text = font.render(f"Saldo: {jugador.saldo}", True, WHITE)
        screen.blit(saldo_text, (x, y + 40))

# Mostrar el estado de todos los jugadores
def mostrar_estado_jugadores(jugadores):
    for jugador in jugadores:
        jugador.mostrar_fichas()
        print()

# Variables para el giro de la ruleta
rotation_angle = 0  # Ángulo inicial de rotación
is_spinning = False  # Estado de la ruleta
spin_speed = 20  # Velocidad inicial de giro
min_deceleration = 0.90  # Límite mínimo de desaceleración
max_deceleration = 0.99  # Límite máximo de desaceleración
deceleration = random.uniform(min_deceleration, max_deceleration)  # Desaceleración aleatoria
# Desaceleración aleatoria
  # Factor de desaceleración

# Configuración del botón
button_rect = pygame.Rect(500, 700, 200, 50)  # Rectángulo del botón

# Función para dibujar la tabla de ruleta
def draw_table():
    # Dibujar el número 0 en una celda separada con borde blanco
    pygame.draw.rect(screen, GREEN2, (50, 50, CELL_WIDTH, CELL_HEIGHT))
    pygame.draw.rect(screen, WHITE, (50, 50, CELL_WIDTH, CELL_HEIGHT), 3)  # Borde blanco alrededor del 0
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
def draw_table2(): 
    rows = 3
    cols = 1
    start_x = 360
    start_y = 50


    
    # Dibujar las celdas de la tabla
    for row in range(rows):
        for col in range(cols):
            # Coordenadas de cada celda
            x = start_x + col * CELL_WIDTH2
            y = start_y + row * CELL_HEIGHT2

            # Dibujar el rectángulo de la celda
            pygame.draw.rect(screen, BLACK, (x, y, CELL_WIDTH2, CELL_HEIGHT2))
            pygame.draw.rect(screen, WHITE, (x, y, CELL_WIDTH2, CELL_HEIGHT2), 2)  # Borde blanco
# Función para dibujar un rombo
def draw_diamond(x, y, color):
    # Coordenadas del rombo
    puntos = [(x, y - 35), (x + 15, y), (x, y + 35), (x - 15, y)]
    pygame.draw.polygon(screen, color, puntos)

def draw_table3(): 
    rows = 6
    cols = 1
    start_x = 430
    start_y = 50
    # Dibujar las celdas de la tabla
    for row in range(rows):
        for col in range(cols):
            # Coordenadas de cada celda
            x = start_x + col * CELL_WIDTH3
            y = start_y + row * CELL_HEIGHT3

            # Dibujar el rectángulo de la celda
            pygame.draw.rect(screen, GREEN, (x, y, CELL_WIDTH3, CELL_HEIGHT3))
            pygame.draw.rect(screen, WHITE, (x, y, CELL_WIDTH3, CELL_HEIGHT3), 2)  # Borde blanco

            #Dibujar Rombos tercera y cuarta
            if row == 2: 
                draw_diamond(x + CELL_WIDTH3 // 2, y + CELL_HEIGHT3// 2 , RED)
            if row == 3: 
                draw_diamond(x + CELL_WIDTH3 // 2, y +  CELL_HEIGHT3 // 2, BLACK)

            # Escribir 'par' en la segunda celda (fila 1)
            if row == 1:  # Celda 1 (primera fila)
                text = font.render("PAR", True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_WIDTH3 // 2, y + CELL_HEIGHT3 // 2))
                screen.blit(text, text_rect)
            # Escribir 'impar' en la quinta celda (fila 1)
            if row == 4:  # Celda 1 (primera fila)
                text = font.render("IMPAR", True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_WIDTH3 // 2, y + CELL_HEIGHT3 // 2))
                screen.blit(text, text_rect)
            # Escribir '1-18' en la primera celda (fila 1)
            if row == 0:  # Celda 1 (primera fila)
                text = font.render("1-18", True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_WIDTH3 // 2, y + CELL_HEIGHT3 // 2))
                screen.blit(text, text_rect)
             # Escribir '1-18' en la primera celda (fila 1)
            if row == 5:  # Celda 1 (primera fila)
                text = font.render("1-19", True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_WIDTH3 // 2, y + CELL_HEIGHT3 // 2))
                screen.blit(text, text_rect)
    
    
# Función para realizar apuestas
# Función para realizar apuestas
def realizar_apuestas(jugadores):
    for jugador in jugadores:
        print(f"\nJugador: {jugador.nombre}")
        print(f"Saldo disponible: {jugador.saldo}")
        
        # Apuesta a números
        apuesta_numeros = input("Introduce los números a apostar (separados por comas, ej: 5,7,9): ")
        numeros = [int(n) for n in apuesta_numeros.split(",") if n.isdigit()]
        cantidad_numeros = int(input("Cantidad de unidades por número: "))
        if cantidad_numeros * len(numeros) <= jugador.saldo:
            jugador.saldo -= cantidad_numeros * len(numeros)
            jugador.apuestas.append(("numeros", numeros, cantidad_numeros))
        else:
            print("Saldo insuficiente para esta apuesta!")

        # Apuesta a color
        apuesta_color = input("Introduce el color a apostar (negre o vermell): ").lower()
        cantidad_color = int(input("Cantidad de unidades para el color: "))
        if apuesta_color in ["negre", "vermell"] and cantidad_color <= jugador.saldo:
            jugador.saldo -= cantidad_color
            jugador.apuestas.append(("color", apuesta_color, cantidad_color))
        else:
            print("Color no válido o saldo insuficiente!")

        # Apuesta a paridad
        apuesta_paridad = input("Introduce tipo (parell o senar): ").lower()
        cantidad_paridad = int(input("Cantidad de unidades: "))
        if apuesta_paridad in ["parell", "senar"] and cantidad_paridad <= jugador.saldo:
            jugador.saldo -= cantidad_paridad
            jugador.apuestas.append(("paritat", apuesta_paridad, cantidad_paridad))
        else:
            print("Tipo no válido o saldo insuficiente!")

        # Apuesta a columna
        apuesta_columna = input("Introduce columna (1, 2 o 3): ")
        cantidad_columna = int(input("Cantidad de unidades: "))
        if apuesta_columna in ["1", "2", "3"] and cantidad_columna <= jugador.saldo:
            jugador.saldo -= cantidad_columna
            jugador.apuestas.append(("columna", apuesta_columna, cantidad_columna))
        else:
            print("Columna no válida o saldo insuficiente!")


# Función para dibujar la ruleta circular con colores correspondientes
def draw_roulette(winning_number=None, rotation=0):
    center = (950, 230)
    radius = 200
    num_sectors = len(NUMEROS)
    angle_per_sector = 360 / num_sectors

    pygame.draw.circle(screen, BLACK, center, radius + 8)
    pygame.draw.circle(screen, WHITE, center, radius + 8, 3)

    # Dibujar los sectores de la ruleta con la rotación aplicada
    for i, num in enumerate(NUMEROS):
        start_angle = math.radians(rotation + i * angle_per_sector)
        end_angle = math.radians(rotation + (i + 1) * angle_per_sector)
        color = COLORS[num]
        
        # Dibujar cada sector
        points = [center]
        for angle in range(int(start_angle * 180 / math.pi), int(end_angle * 180 / math.pi) + 1):
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] - radius * math.sin(math.radians(angle))
            points.append((x, y))
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 1)  # Borde de cada sector

    # Dibujar los números encima de los sectores (rotados)
    for i, num in enumerate(NUMEROS):
        angle = math.radians(rotation + i * angle_per_sector + angle_per_sector / 2)
        x = center[0] + (radius - 30) * math.cos(angle)
        y = center[1] - (radius - 30) * math.sin(angle)
        text = font.render(str(num), True, WHITE if COLORS[num] != BLACK else WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


    # Dibujar el número ganador si la ruleta se detiene
    if winning_number is not None and not is_spinning:
    # Dibujar un círculo rojo en el centro para resaltar
        pygame.draw.circle(screen, RED, center, 30)
        # Renderizar el número ganador en el centro
        winning_text = font.render(str(winning_number), True, WHITE)
        screen.blit(winning_text, (center[0] - winning_text.get_width() // 2,
                               center[1] - winning_text.get_height() // 2))

button_rect = pygame.Rect(850, 450, 200, 50)

# Función para dibujar el botón
def draw_button():
    pygame.draw.rect(screen, BLACK, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 3)
    text = button_font.render("Girar", True, WHITE)
    screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                       button_rect.y + (button_rect.height - text.get_height()) // 2))
   
# Bucle principal del juego
running = True
winning_number = None
current_player = 0  # Índice del jugador actual

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not is_spinning:
                # Seleccionar al jugador actual
                jugador_actual = jugadores[current_player]
                winning_number, _ = ruleta.girar()
                is_spinning = True
                spin_speed = 20  # Reiniciar la velocidad inicial

                # Avanzar al siguiente jugador
                current_player = (current_player + 1) % len(jugadores)

    # Dibujar el fondo
    screen.fill(GREEN)
    
    # Dibujar la tabla y ruleta
    draw_table()
    draw_table2()
    draw_table3()

    # Actualizar la ruleta con animación
    if is_spinning:
        rotation_angle += spin_speed
        spin_speed *= deceleration  # Reducir gradualmente la velocidad
        if spin_speed < 0.1:  # Cuando la velocidad es muy baja, detener
            is_spinning = False
            rotation_angle = winning_number * (360 / len(NUMEROS))  # Ajustar al número ganador

    draw_roulette(winning_number, rotation_angle)

    # Dibujar los jugadores y sus fichas
    draw_players(jugadores)
    # Llamar antes del giro
    realizar_apuestas(jugadores)

    # Dibujar el botón
    draw_button()
    
    # Actualizar la pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()




