import os
import sys
import time
import json
import signal
import random
import argparse
import threading
import subprocess
import configparser

sys.path.insert(1, './code')
import init
import flags

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

for flag in flags:
    print(flag.getFlag())

#Crear población inicial
