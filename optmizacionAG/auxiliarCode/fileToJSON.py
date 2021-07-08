import json
import sys
import os
import time
import signal
import sys

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
    time.sleep(0.5)


data['rango'] = []


def crearFlagRango(flag, min, max):
    data['rango'].append({
        'flag': flag,
        'min': min,
        'max': max
    })
    print('Flag ' + flag + ' con rango [' + min + ', ' + max + '] añadida con éxito.')
    time.sleep(0.5)


data['Intervalo'] = []


def crearFlagIntervalo(flag, intervalo):
    data['Intervalo'].append({
        'flag': flag,
        'intervalo': intervalo
    })
    print('Flag ' + flag + ' con intervalo [' + intervalo + '] añadida con éxito.')
    time.sleep(0.5)

def escribir(fichero):
    with open(fichero, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print('Flags escritas en: ' + fichero)

def main():
    archivoOrigen = sys.argv[1]
    print('Archivo origen: ' + archivoOrigen)
    archivoDestino = input('Archivo destino: ' )
    origen = open(archivoOrigen, 'r')
    for line in origen:
        partes = line.split(',')
        if partes[0] == 'simple':
            crearFlagBinaria(partes[1])
        elif partes[0] == 'intervalo':
            flag = partes[1]
            intervalo = str(partes[2])
            for data in partes[3:-1]:
                if data.isalnum():
                    intervalo += ',' + str(data)
            crearFlagIntervalo(flag, intervalo)
        elif partes[0] == 'rango':
            crearFlagRango(partes[1],partes[2],partes[3])

    escribir(archivoDestino)

if __name__ == "__main__":
    main()