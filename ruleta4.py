#!/usr/bin/env python3
import pygame
import sys
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruleta")

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
font = pygame.font.SysFont("Arial", 20)
font_numero_winner = pygame.font.SysFont("Arial", 50)
button_font = pygame.font.SysFont("Arial", 28)

# Configuración de la tabla de ruleta
numbers = [
    ('0', GREEN2), ('1', RED), ('2', BLACK), ('3', RED), ('4', BLACK), ('5', RED), ('6', BLACK),
    ('7', RED), ('8', BLACK), ('9', RED), ('10', BLACK), ('11', BLACK), ('12', RED),
    ('13', BLACK), ('14', RED), ('15', BLACK), ('16', RED), ('17', BLACK), ('18', RED),
    ('19', RED), ('20', BLACK), ('21', RED), ('22', BLACK), ('23', RED), ('24', BLACK),
    ('25', RED), ('26', BLACK), ('27', RED), ('28', BLACK), ('29', BLACK), ('30', RED),
    ('31', BLACK), ('32', RED), ('33', BLACK), ('34', RED), ('35', BLACK), ('36', RED)
]

# Tamaño de cada celda en la tabla
CELL_WIDTH = 80
CELL_HEIGHT = 40
CELL_WIDTH2 = 80
CELL_HEIGHT2 = 160
CELL_WIDTH3 = 80
CELL_HEIGHT3 = 80
CELL_WIDTH4 = 80
CELL_HEIGHT4 = 60

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

# Clase para representar a los jugadores
# Clase Jugador adaptada
class Jugador:
    def __init__(self, nombre, color, saldo=100):
        self.nombre = nombre
        self.color = color
        self.saldo = saldo
        self.fichas = {"005": 0, "010": 0, "020": 0, "050": 0, "100": 0}
        self.actualizar_fichas()

    def actualizar_fichas(self):
        """
        Actualiza las fichas del jugador reorganizando el saldo disponible.
        """
        valores = ["100", "050", "020", "010", "005"]
        restante = self.saldo
        for valor in valores:
            ficha_valor = int(valor)
            self.fichas[valor] = restante // ficha_valor
            restante %= ficha_valor

    def saldo_total(self):
        """
        Devuelve el saldo total basado en las fichas del jugador.
        """
        return sum(int(valor) * cantidad for valor, cantidad in self.fichas.items())
    



# Crear jugadores
jugadores = [
    Jugador("Taronja", (255, 165, 0)),  # Naranja
    Jugador("Lila", (128, 0, 128)),     # Lila
    Jugador("Blau", (0, 0, 255))        # Azul
]


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

def draw_bets():
    for jugador, apuestas_jugador in apuestas.items():
        for tipo, valor, detalle in apuestas_jugador:
            if tipo == "número":  # Apuesta en un número
                col = (detalle - 1) % 3
                row = (detalle - 1) // 3
                x = 150 + col * 80 + 40
                y = 50 + row * 40 + 20

                # Dibujar la ficha
                pygame.draw.circle(screen, jugador.color, (x, y), 15)

                # Mostrar el valor de la ficha
                texto = font.render(f"{valor:03}", True, WHITE)
                screen.blit(texto, (x - texto.get_width() // 2, y - texto.get_height() // 2))


def draw_table2(): 
    rows = 3
    cols = 1
    start_x = 390
    start_y = 50


    
    # Dibujar las celdas de la tabla
    for row in range(rows):
        for col in range(cols):
            # Coordenadas de cada celda
            x = start_x + col * CELL_WIDTH2
            y = start_y + row * CELL_HEIGHT2

            # Dibujar el rectángulo de la celda
            pygame.draw.rect(screen, GREEN, (x, y, CELL_WIDTH2, CELL_HEIGHT2))
            pygame.draw.rect(screen, WHITE, (x, y, CELL_WIDTH2, CELL_HEIGHT2), 2)  # Borde blanco

            # Escribir '1st 12' en la segunda celda (fila 1)
            if row == 0:  # Celda 1 (primera fila)
                text = font.render("1st 12", True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_WIDTH2 // 2, y + CELL_HEIGHT2 // 2))
                screen.blit(text, text_rect)
            # Escribir '1st 12' en la segunda celda (fila 1)
            if row == 1:  # Celda 1 (primera fila)
                text = font.render("2nd 12", True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_WIDTH2 // 2, y + CELL_HEIGHT2 // 2))
                screen.blit(text, text_rect)
            # Escribir '1st 12' en la segunda celda (fila 1)
            if row == 2:  # Celda 1 (primera fila)
                text = font.render("3rd 12", True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_WIDTH2 // 2, y + CELL_HEIGHT2 // 2))
                screen.blit(text, text_rect)
# Función para dibujar un rombo
def draw_diamond(x, y, color):
    # Coordenadas del rombo
    puntos = [(x, y - 35), (x + 15, y), (x, y + 35), (x - 15, y)]
    pygame.draw.polygon(screen, color, puntos)

def draw_table3(): 
    rows = 6
    cols = 1
    start_x = 470
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
def draw_table4(): 
    rows = 1
    cols = 3
    start_x = 150
    start_y = 530
# Dibujar las celdas de la tabla
    for row in range(rows):
        for col in range(cols):
            # Coordenadas de cada celda
            x = start_x + col * CELL_WIDTH
            y = start_y + row * CELL_HEIGHT

            # Dibujar el fondo negro de la celda
            pygame.draw.rect(screen, GREEN, (x, y, CELL_WIDTH4, CELL_HEIGHT4))

            # Dibujar el borde blanco de la celda
            pygame.draw.rect(screen, WHITE, (x, y, CELL_WIDTH4, CELL_HEIGHT4), 3)  # Borde blanco
            # Escribir '2 to1' en cada celda
            text = font.render("2 to 1", True, WHITE)
            text_rect = text.get_rect(center=(x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2))
            screen.blit(text, text_rect)

def draw_apuestas():
    for jugador, apuestas_jugador in apuestas.items():
        for tipo, valor, detalle in apuestas_jugador:
            if tipo == "número":  # Apuesta a un número
                col = (detalle - 1) % 3
                row = (detalle - 1) // 3
                x = 150 + col * CELL_WIDTH + CELL_WIDTH // 2
                y = 50 + row * CELL_HEIGHT + CELL_HEIGHT // 2
            elif tipo == "color":  # Apuesta a un color
                x = 500
                y = 75 if detalle == RED else 175
            elif tipo == "columna":  # Apuesta a una columna
                x = 430
                y = 75 + (detalle - 1) * CELL_HEIGHT2

            # Dibujar ficha
            pygame.draw.circle(screen, jugador.color, (x, y), 15)
            texto = font.render(f"{valor:03}", True, WHITE)
            screen.blit(texto, (x - texto.get_width() // 2, y - texto.get_height() // 2))


# Función para dibujar la ruleta circular con colores correspondientes
def draw_roulette(winning_number, rotation):
    center = (950, 265)
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

  

    # Dibujar el número ganador si está definido
    if winning_number is not None and not is_spinning:
        pygame.draw.circle(screen, WHITE, (center[0], center[1] - radius - -200), 50)  # Círculo blanco encima de la ruleta
        winner_text = font_numero_winner.render(str(winning_number), True, BLACK)  # Número ganador en negro
        screen.blit(winner_text, (center[0] - winner_text.get_width() // 2, 
                                  center[1] - radius - -200 - winner_text.get_height() // 2))
        
def draw_jugadores():
    start_y = 750  # Área para jugadores
    for i, jugador in enumerate(jugadores):
        x = 50 + i * 400
        y = start_y

        # Dibujar nombre del jugador
        pygame.draw.rect(screen, jugador.color, (x, y, 300, 100))  # Fondo
        nombre_texto = font.render(jugador.nombre, True, WHITE)
        screen.blit(nombre_texto, (x + 10, y + 10))

        # Dibujar fichas del jugador
        fichas_y = y + 40
        for valor, cantidad in jugador.fichas.items():
            ficha_texto = font.render(f"{valor:03} x {cantidad}", True, WHITE)
            screen.blit(ficha_texto, (x + 10, fichas_y))
            fichas_y += 20

# Variables para apuestas
apuestas_hechas = False  # Indica si al menos un jugador ha hecho apuestas
apuestas = {jugador.nombre: [] for jugador in jugadores}
ficha_seleccionada = None
jugador_actual = None
for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
    if event.type == pygame.QUIT:
        running = False
        # Detectar clics en las fichas de los jugadores
        for jugador in jugadores:
            x = 50 + jugadores.index(jugador) * 400
            fichas_y = 640  # Coordenada inicial de las fichas
            for valor, cantidad in jugador.fichas.items():
                if cantidad > 0:  # Solo detecta si hay fichas disponibles
                    ficha_centro = (x + 20, fichas_y + 10)
                    if math.hypot(mouse_x - ficha_centro[0], mouse_y - ficha_centro[1]) <= 10:  # Círculo clicable
                        ficha_seleccionada = valor
                        jugador_actual = jugador
                        print(f"Seleccionada ficha de {valor} por {jugador.nombre}")
                        break
                fichas_y += 30

    # Al soltar la ficha, registrar la apuesta
    if event.type == pygame.MOUSEBUTTONUP and ficha_seleccionada:
        mouse_x, mouse_y = event.pos
        # Detectar si se soltó en un número válido
        if 150 <= mouse_x <= 390 and 50 <= mouse_y <= 530:
            col = (mouse_x - 150) // 80
            row = (mouse_y - 50) // 40
            numero = row * 3 + col + 1
            apuestas[jugador_actual.nombre].append(("número", ficha_seleccionada, numero))
            jugador_actual.apostar(ficha_seleccionada)
            apuestas_hechas = True  # Marcar que se realizó una apuesta
            if jugador_actual.saldo >= ficha_seleccionada:
                apuestas[jugador_actual.nombre].append(("número", ficha_seleccionada, numero))
                jugador_actual.saldo -= ficha_seleccionada
                jugador_actual.actualizar_fichas()
                apuestas_hechas = True
            else:
                print(f"{jugador_actual.nombre} no tiene suficiente saldo para apostar.")
        # Detectar si se soltó en "Rojo" o "Negro"
        elif 470 <= mouse_x <= 550 and 50 <= mouse_y <= 130:
            apuestas[jugador_actual.nombre].append(("color", ficha_seleccionada, RED))
            jugador_actual.apostar(ficha_seleccionada)
            apuestas_hechas = True
        elif 470 <= mouse_x <= 550 and 130 <= mouse_y <= 210:
            apuestas[jugador_actual.nombre].append(("color", ficha_seleccionada, BLACK))
            jugador_actual.apostar(ficha_seleccionada)
            apuestas_hechas = True

        if 150 <= mouse_x <= 390 and 50 <= mouse_y <= 530:
            col = (mouse_x - 150) // 80  # Columna
            row = (mouse_y - 50) // 40   # Fila
            numero = row * 3 + col + 1   # Calcular el número basado en fila y columna

        # Registrar la apuesta
        if jugador_actual.saldo >= ficha_seleccionada:
            apuestas[jugador_actual.nombre].append(("número", ficha_seleccionada, numero))
            jugador_actual.saldo -= ficha_seleccionada
            jugador_actual.actualizar_fichas()
            apuestas_hechas = True
            print(f"{jugador_actual.nombre} apostó {ficha_seleccionada} al número {numero}")
        else:
            print(f"{jugador_actual.nombre} no tiene suficiente saldo para apostar.")

        # Registrar la apuesta
        apuestas[jugador_actual.nombre].append(("número", ficha_seleccionada, numero))
        jugador_actual.saldo -= ficha_seleccionada
        jugador_actual.actualizar_fichas()
        apuestas_hechas = True

        print(f"{jugador_actual.nombre} apostó {ficha_seleccionada} al número {numero}")


        # Resetear selección
        ficha_seleccionada = None
    # Colocar la ficha en un área de apuesta
if event.type == pygame.MOUSEBUTTONUP and ficha_seleccionada:
    mouse_x, mouse_y = event.pos
        # Apuesta en números
    if 150 <= mouse_x <= 390 and 50 <= mouse_y <= 530:  # Celdas numéricas
        col = (mouse_x - 150) // 80
        row = (mouse_y - 50) // 40
        numero = row * 3 + col + 1
        apuestas[jugador_actual.nombre].append(("número", ficha_seleccionada, numero))
        jugador_actual.saldo -= ficha_seleccionada
        jugador_actual.actualizar_fichas()
        apuestas_hechas = True

    # Apuesta en colores
    elif 470 <= mouse_x <= 550 and 50 <= mouse_y <= 210:  # Rojo o Negro
        color = RED if mouse_y < 130 else BLACK
        apuestas[jugador_actual.nombre].append(("color", ficha_seleccionada, color))
        jugador_actual.saldo -= ficha_seleccionada
        jugador_actual.actualizar_fichas()
        apuestas_hechas = True

    # Resetear ficha seleccionada
    ficha_seleccionada = None
    jugador_actual = None
    

button_rect = pygame.Rect(850, 480, 200, 50)

# Función para dibujar el botón
def draw_button():
    pygame.draw.rect(screen, GREEN, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 3)
    text = button_font.render("Girar", True, WHITE)
    screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                       button_rect.y + (button_rect.height - text.get_height()) // 2))
def finDelJuego():
    print(Back.BLACK + Fore.LIGHTWHITE_EX + "Fin del juego")
    print("Jugaste un total de", contador_total, "apuestas")
    print("Tu saldo final es de $", fondo)
    print("Gracias por jugar!" + Fore.RESET + Back.RESET)



# Bucle principal del juego
running = True
winning_number = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos 
            if button_rect.collidepoint(event.pos) and not is_spinning:
                winning_number, _ = ruleta.girar()
                is_spinning = True
                spin_speed = 20  # Reiniciar la velocidad inicial
        
        # Detectar presionar la tecla Enter
        if event.type == pygame.KEYDOWN:
            if jugador_actual and ficha_seleccionada:
                if event.unicode.isdigit():  # Apuesta en número específico
                    numero = int(event.unicode)
                    if 0 <= numero <= 36:
                        apuestas[jugador_actual.nombre].append(("número", ficha_seleccionada, numero))
                        jugador_actual.saldo -= ficha_seleccionada
                        jugador_actual.actualizar_fichas()
                        apuestas_hechas = True
                elif event.unicode.lower() in ["r", "n"]:  # Apuesta en rojo o negro
                    color = RED if event.unicode.lower() == "r" else BLACK
                    apuestas[jugador_actual.nombre].append(("color", ficha_seleccionada, color))
                    jugador_actual.saldo -= ficha_seleccionada
                    jugador_actual.actualizar_fichas()
                    apuestas_hechas = True
                elif event.unicode in ["1", "2", "3"]:  # Apuesta en columnas
                    columna = int(event.unicode)
                    apuestas[jugador_actual.nombre].append(("columna", ficha_seleccionada, columna))
                    jugador_actual.saldo -= ficha_seleccionada
                    jugador_actual.actualizar_fichas()
                    apuestas_hechas = True
                # Resetear ficha seleccionada
                ficha_seleccionada = None

    
    # Verificar si todos los jugadores están arruinados
    if all(jugador.saldo <= 0 for jugador in jugadores):
        print("¡Todos los jugadores están arruinados! Fin del juego.")
        running = False


    # Dibujar el fondo
    screen.fill(GREEN)
    
    # Dibujar la tabla de ruleta
    draw_table()
    draw_table2()
    draw_table3()
    draw_table4()

    # Actualizar la ruleta con animación
    # En el bucle principal, después de `if is_spinning:`
    if is_spinning:
        rotation_angle += spin_speed
        spin_speed *= deceleration
        if spin_speed < 0.1:  # Parar el giro
            is_spinning = False
            for jugador in jugadores:
                for tipo, valor, detalle in apuestas[jugador.nombre]:
                    if tipo == "número" and detalle == ruleta.resultado:
                        jugador.saldo += valor * 35
                    elif tipo == "color" and detalle == COLORS[ruleta.resultado]:
                        jugador.saldo += valor * 2
                    elif tipo == "columna" and (ruleta.resultado - 1) // 12 + 1 == detalle:
                        jugador.saldo += valor * 3
                apuestas[jugador.nombre] = []  # Limpiar apuestas después de procesarlas
            apuestas_hechas = False  # Resetea el estado de apuestas
    if apuestas_hechas:  # Solo girar si hay apuestas
        winning_number, _ = ruleta.girar()
        is_spinning = True
        spin_speed = 20  # Reiniciar la velocidad inicial
    else:
        print("Debe realizar al menos una apuesta antes de girar.")

    
    # Resetear estado de la ruleta
    is_spinning = False
    apuestas_hechas = False
    
    draw_roulette(winning_number, rotation_angle)

    # Dibujar el botón
    draw_button()
    
    # Actualizar la pantalla
    pygame.display.flip()

        # Resetear apuestas
    for jugador in jugadores:
        jugador.actualizar_fichas()

# Salir de Pygame
pygame.quit()
sys.exit()