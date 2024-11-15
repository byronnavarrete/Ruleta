#!/usr/bin/env python3
import pygame
import random
import math

# Constants del joc
NOMBRES = list(range(37))  # De 0 a 36
COLORS = {0: "verd", **{n: "vermell" if n % 2 else "negre" for n in range(1, 37)}}
COLUMNES = {1: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
            2: [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
            3: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]}
FITXES_VALORS = [5, 10, 20, 50, 100]
AMPLADA, ALCADA = 800, 600

class Jugador:
    def __init__(self, nom, saldo=100):
        self.nom = nom
        self.saldo = saldo
        self.fitxes = {val: 0 for val in FITXES_VALORS}
        self._distribuir_fitxes()
        self.apostes = []  # Ex. [(tipus, valor)]

    def _distribuir_fitxes(self):
        restant = self.saldo
        for val in sorted(FITXES_VALORS, reverse=True):
            self.fitxes[val], restant = divmod(restant, val)

    def apostar(self, quantitat, tipus_aposta):
        if quantitat > self.saldo:
            raise ValueError(f"{self.nom} no té saldo suficient!")
        self.saldo -= quantitat
        self.apostes.append((tipus_aposta, quantitat))

    def afegir_guanys(self, quantitat):
        self.saldo += quantitat
        self._distribuir_fitxes()

    def dibuixar_fitxes(screen, jugador, pos_x, pos_y):
    # Exemple per dibuixar les fitxes d'un jugador
        font = pygame.font.Font(None, 24)
        for valor, quantitat in jugador.fitxes.items():
            for i in range(quantitat):
                # Dibuixar una fitxa de color
                pygame.draw.circle(screen, (255, 165, 0), (pos_x, pos_y), 15)
                pos_y += 30  # Espai entre fitxes
                text = font.render(f"{valor} x {quantitat}", True, (0, 0, 0))
                screen.blit(text, (pos_x + 20, pos_y))


class Ruleta:
    def __init__(self):
        self.resultat = None

    def girar(self):
        self.resultat = random.choice(NOMBRES)
        return self.resultat, COLORS[self.resultat]
    
    def dibuixar_taula_apostes(screen):
    # Espais per apostes
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(50, 450, 100, 50))  # Espai "vermell"
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 450, 100, 50))  # Espai "negre"
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(250, 450, 100, 50))  # Espai "parell"
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(350, 450, 100, 50))  # Espai "senar"
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(450, 450, 100, 50))  # Espai "columna1"
        # Afegeix més espais per columna 2 i 3...


class Partida:
    def __init__(self):
        self.ruleta = Ruleta()
        self.jugadors = [Jugador("Taronja"), Jugador("Lila"), Jugador("Blau")]
        self.historial = []

    def calcular_guanys(self, resultat):
        for jugador in self.jugadors:
            for tipus, quantitat in jugador.apostes:
                # Número exacte
                if tipus == "numero" and resultat[0] == tipus:
                    jugador.afegir_guanys(quantitat * 35)
                # Color (vermell/negre)
                elif tipus == "color" and resultat[1] == tipus:
                    jugador.afegir_guanys(quantitat * 2)
                # Parell/Senar
                elif tipus == "parell" and resultat[0] != 0 and resultat[0] % 2 == 0:
                    jugador.afegir_guanys(quantitat * 2)
                elif tipus == "senar" and resultat[0] % 2 != 0:
                    jugador.afegir_guanys(quantitat * 2)
                # Columna
                elif tipus in ["columna1", "columna2", "columna3"]:
                    columna = COLUMNES[int(tipus[-1])]
                    if resultat[0] in columna:
                        jugador.afegir_guanys(quantitat * 3)
            jugador.apostes.clear()

    def jugar_tirada(self):
        resultat = self.ruleta.girar()
        self.calcular_guanys(resultat)
        self.historial.append({"resultat": resultat, "jugadors": [(j.nom, j.saldo) for j in self.jugadors]})

    

# Funció per mostrar moviment de fitxes
def moure_fitxes(screen, origen, desti, color):
    x1, y1 = origen
    x2, y2 = desti
    passos = 20
    for i in range(passos):
        x = x1 + (x2 - x1) * i / passos
        y = y1 + (y2 - y1) * i / passos
        pygame.draw.circle(screen, color, (int(x), int(y)), 10)
        pygame.display.flip()
        pygame.time.delay(30)

def moure_fitxa(screen, jugador, mouse_x, mouse_y):
    # Exemple per detectar el moviment d'una fitxa
    if jugador.fitxes[5] > 0:  # Si el jugador té fitxes de valor 5
        pygame.draw.circle(screen, (255, 165, 0), (mouse_x, mouse_y), 15)

def moure_fitxes_cap_a_banca(screen, origen, banc):
    # Mou les fitxes cap a la banca
    pygame.draw.circle(screen, (0, 0, 0), banc, 15)


def mostrar_historial(screen, historial):
    font = pygame.font.Font(None, 24)
    for i, tirada in enumerate(historial):
        text = font.render(f"Tirada {i+1}: {tirada['resultat']}", True, (255, 255, 255))
        screen.blit(text, (50, 100 + i*30))


# Interfície gràfica
def dibuixar_ruleta(screen, resultat=None):
    pygame.draw.circle(screen, (200, 200, 200), (400, 300), 200, 0)
    font = pygame.font.Font(None, 24)
    for i, num in enumerate(NOMBRES):
        angle = math.radians(i * (360 / len(NOMBRES)))
        x = 400 + 180 * math.cos(angle)
        y = 300 - 180 * math.sin(angle)
        text = font.render(str(num), True, (0, 0, 0))
        screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    if resultat:
        pygame.draw.line(screen, (255, 0, 0), (400, 300), (400, 100), 5)

def girar_ruleta_decreixent(screen):
    angle = 0
    velocitat = 0.1
    while velocitat > 0:
        angle += velocitat
        velocitat *= 0.99  # Decelerar
        pygame.draw.circle(screen, (200, 200, 200), (400, 300), 200, 0)  # Dibuixar ruleta
        pygame.draw.arc(screen, (255, 0, 0), (200, 200, 400, 400), 0, math.radians(angle), 5)
        pygame.display.flip()
        pygame.time.delay(10)


def joc_grafic():
    pygame.init()
    screen = pygame.display.set_mode((AMPLADA, ALCADA))
    pygame.display.set_caption("Ruleta de Casino")
    clock = pygame.time.Clock()
    partida = Partida()
    resultat = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                resultat = partida.ruleta.girar()
                origen = (400, 300)
                desti = (600, 100)
                moure_fitxes(screen, origen, desti, (255, 0, 0))

        screen.fill((0, 128, 0))
        dibuixar_ruleta(screen, resultat)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    joc_grafic()
