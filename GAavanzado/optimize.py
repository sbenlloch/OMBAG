import os
import sys
import time
import json
import copy
import signal
import random
import argparse
import threading
import subprocess
import configparser

sys.path.insert(1, './code')
import init
import flags
import cromosoma
import auxiliar

def signal_handler(sig, frame):
    print('\n[!]Saliendo...')
    os._exit(1)


signal.signal(signal.SIGINT, signal_handler)

#Argumentos de programa
argparser = argparse.ArgumentParser()
argparser.add_argument("-p", "--program", dest="program",
                        help="Programa a optimizar")
argparser.add_argument("-a", "--arguments", dest="arguments",
                        help="Aregumentos del programa para hacer pruebas")
args = argparser.parse_args()

parser = configparser.ConfigParser()
parser.read('conf.ini')
#Leer e inicializar objetis Flag
path = parser['Flags']['Path']

with open(path) as file:
    flags = init.inicializacionFlags(file)

#Crear poblacion inicial aleatoria con tamaño indicado en el archivo de configuracion
tamaño_inicial = int(parser['Settings']['Tamaño_Inicial'])
poblacionInicial = init.generarPoblacionAleatoria(tamaño_inicial, flags)

#Creacion de directorio para jerarquía inicial
path_inicial = parser['Test']['Path_Inicio']
directorioBase = path_inicial + 'Ejecucion' + init.tiempo()
if not os.path.isdir(directorioBase):
    os.system('mkdir ' + directorioBase)
else:
    raise ValueError('[!]Error, archivo inicial ya existe')

#Bucle donde se compila, testea, selecciona y se genera la siguiente generacion,
#comprobando que no se cumplan los limites impuestos en conf.ini

#while True: