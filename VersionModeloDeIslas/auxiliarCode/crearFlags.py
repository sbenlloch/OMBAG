import json
import sys
import os
import time
import signal


def signal_handler(sig, frame):
    print('\n[!]Saliendo y cancelando creación de archivo.')
    os._exit(1)


signal.signal(signal.SIGINT, signal_handler)

data = {}
data['binarias'] = []


def crearFlagBinaria(flag):
    data['binarias'].append({
        'flag': flag
    })
    print('Flag ' + flag + ' añadida con éxito.')
    time.sleep(1)


data['rango'] = []


def crearFlagRango(flag, min, max):
    data['rango'].append({
        'flag': flag,
        'min': min,
        'max': max
    })
    print('Flag ' + flag + ' con rango [' + min + ', ' + max + '] añadida con éxito.')
    time.sleep(2)


data['Intervalo'] = []


def crearFlagIntervalo(flag, intervalo):
    data['Intervalo'].append({
        'flag': flag,
        'intervalo': intervalo
    })
    print('Flag ' + flag + ' con intervalo [' + intervalo + '] añadida con éxito.')
    time.sleep(2)


def cabecera():
    os.system('clear')
    print('\n' + '╔' + '═'*50 + '╗')
    print(' '*9 + 'Programa para crear lista de flags' + ' ' * 9)
    print('╚' + '═'*50 + '╝' + '\n')

def cabeceraPers(tipo):
    os.system('clear')
    print('\n' + '╔' + '═'*50 + '╗')
    print(' '*8 + 'Programa para crear flag tipo ' + tipo + ' ' * 8)
    print('╚' + '═'*50 + '╝' + '\n')

def escribir(fichero):
    with open(fichero, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print('Flags escritas en: ' + fichero)

def main():
    while True:

        while True:
            cabecera()
            print('Selecciona tipo de flags a añadir:\n\t(1) Flag Simple. \n\t(2) Flag con rango de valores numéricos posibles. \n\t(3) Flag con intervalo de valores posibles. \n\t(-1)Salir y crear archivo con flags añadidas. \n')

            try:
                tipo = int(
                    input('Tipo de Flag a crear y añadir[ 1, 2, 3] o [-1] para salir: ') or 4)
            except:
                tipo = 4

            if tipo != 1 and tipo != 2 and tipo != 3 and tipo != -1:
                print('Tipo invalido, debe estar entre [1, 2, 3] o [-1] para salir.')
                time.sleep(1)
            else:
                break

        if tipo == -1:
            break
        elif tipo == 1:
            cabeceraPers('simple')
            nombreflag = input('Introduzca la flag simple completa: ')
            crearFlagBinaria(nombreflag)
        elif tipo == 2:
            cabeceraPers('rango')
            nombreflag = input('Introduzca la flag con el \'=\': ')
            if '=' not in nombreflag:
                print('Se va a añadir un \'=\' al final de la flag para poder asignar el rango.')
                nombreflag = nombreflag + '='
            minimo = input('Valor mínimo del rango: ')
            maximo = input('Valor máximo del rango: ')
            crearFlagRango(nombreflag, minimo, maximo)
        elif tipo == 3:
            cabeceraPers('intervalo')
            nombreflag = input('Introduzca la flag con el \'=\': ')
            if '=' not in nombreflag:
                print('Se va a añadir un \'=\' al final de la flag para poder asignar el valor del intervalo elegido.')
                nombreflag = nombreflag + '='
            intervalo = input('Intervalo, valores continuados de [,] sin espacios: ')
            crearFlagIntervalo(nombreflag, intervalo)
    cabecera()
    nombreFichero = input('Introduce el nombre del fichero a crear: ')
    nombreFichero = nombreFichero + '.json'
    escribir(nombreFichero)


if __name__ == "__main__":
    main()