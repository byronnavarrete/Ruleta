# Importacion de librerias a utilizar
import colorama
import random
import time
from colorama import init, Fore, Back
init()
ruleta = list(range(0, 36, 1))
cero = [0]
rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36]
negros = [2, 4, 6, 7, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 29, 31, 33,35]

print(Back.BLACK + Fore.GREEN + "------------------------------------------------------------------------------------------------")
print("|     Bienvenidos a la ruleta en Python! Elijan su numero, hagan sus apuestas y a jugar!        |")
print("-----------------------------------------------------------------------------------------------------------------------------------------"+ Fore.RESET + Back.RESET)
print(Back.BLACK + Fore.GREEN , cero, Fore.RESET + Back.RESET) 
print(Back.BLACK + Fore.RED , rojos , Fore.RESET + Back.RESET)
print(Back.BLACK + Fore.BLACK , negros , Fore.RESET + Back.RESET)
print(Back.BLACK + Fore.GREEN +"-----------------------------------------------------------------------------------------------------------------------------------------"+ Fore.RESET + Back.RESET)

##############################################################################################


def finDelJuego():
    print(Back.BLACK + Fore.LIGHTWHITE_EX +"Fin del juego")
    print("Jugaste un total de", contador_total, "apuestas")
    print("Tu saldo final es de $", fondo)
    print("Gracias por jugar!" + Fore.RESET + Back.RESET)


fondo_inicial = 1000
fondo = fondo_inicial
juegos_ganados = 0
seguir_jugando = True
contador_total = 0
while fondo > 0 and seguir_jugando:
    numero = int(input(Back.BLACK + Fore.LIGHTWHITE_EX + "Elige tu numero: "))
    if numero < 0 or numero > 36:
        print("El numero tiene que ser entre el 0 y el 36")
        continue
    apuesta = int(input("Elige tu apuesta:$" ))
    if apuesta > fondo:
        print("No tienes suficiente saldo para realizar esta apuesta" + Fore.RESET + Back.RESET)
        continue
    print(Back.BLACK + Fore.GREEN + "-----------------------------------------------------------------------------------------------------------------------------------------"+ Fore.RESET + Back.RESET)
    ganancia = apuesta * 36
    print(Back.BLACK + Fore.LIGHTWHITE_EX + "Se gira la ruleta....")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    aleatorio = random.choice(ruleta)
    print("El numero que salió es el", aleatorio , Fore.RESET + Back.RESET)
    print(Back.BLACK + Fore.GREEN +"-----------------------------------------------------------------------------------------------------------------------------------------"+ Fore.RESET + Back.RESET)
    if numero == int(aleatorio):
        contador_total += 1
        fondo += ganancia
        print(aleatorio)
        print(Back.BLACK + Fore.LIGHTWHITE_EX + "Ganaste! $", apuesta * 36,  Fore.RESET + Back.RESET)
        print("Apuesta N: ", contador_total)
        print("Tu fondo es de $", fondo,  Fore.RESET + Back.RESET)
    else:
        contador_total += 1
        fondo -= apuesta
    print(Back.BLACK + Fore.LIGHTWHITE_EX +"Segui participando")
    print("Apuesta N:", contador_total)
    print("Tu fondo es de $", fondo, Fore.RESET + Back.RESET)
    print(Back.BLACK + Fore.GREEN +"-----------------------------------------------------------------------------------------------------------------------------------------"+ Fore.RESET + Back.RESET)
    respuesta = input(Back.BLACK + Fore.LIGHTWHITE_EX + "Queres seguir jugando? (S/N)" + Fore.RESET + Back.RESET).lower()
    seguir_jugando = respuesta == "s"
print(Back.BLACK + Fore.GREEN +"-----------------------------------------------------------------------------------------------------------------------------------------"+ Fore.RESET + Back.RESET)



finDelJuego()