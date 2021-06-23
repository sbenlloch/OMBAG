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
import norm
import flags
import fitness
import cromosoma
import auxiliar

def signal_handler(sig, frame):
    print('\n\033[0;0m\033[1;31m [!]Saliendo...')
    os._exit(1)
os.system('clear')
print("\033[1;36m", end='')
print('╔' + '═'*66 + '╗')
print(' '*10 + 'Algoritmo Genético v2 para otimizar programas C' + ' '*10)
print('╚' + '═'*66 + '╝' + '\n')
print('\033[2m Puedes cambiar la configuración desde el archivo \033[3mconf.ini\033[0m\033[1;36m\033[2m. También')
print('\033[2m puedes personalizar las flags en el archivo \033[3mflags.json' +
        '\033[0m\033[2m\033[1;36m o indicando')
print(' un nuevo archivo. El resultado de la optimización puede acabar en')
print(' un programa poco estable al tratarse de un proceso de optimización.')
print(' Encontrarás diferentes estadisticas de la optimización en el direc-\n torio base configurado.\n')
signal.signal(signal.SIGINT, signal_handler)

#Argumentos de programa
argparser = argparse.ArgumentParser()
argparser.add_argument("-p", "--programa", dest="program",
                        help="Path absoluto del programa a optimizar")
argparser.add_argument("-a", "--arguments", dest="arguments",
                        help="Argumentos del programa para hacer pruebas")
argparser.add_argument('-i', "--imprimir", dest="imprimir", default=False, action='store_true')
args = argparser.parse_args()

parser = configparser.ConfigParser()
parser.read('conf.ini')

#Leer e inicializar objetis Flag
path = parser['Flags']['Path']
print('\033[0;32m' +' ' + '-'*66 + '\n\n [*]Inicializando flags como objetos')
with open(path) as file:
    flags = init.inicializacionFlags(file)

#Crear poblacion inicial aleatoria con tamaño indicado en el archivo de configuracion
tamaño_inicial = int(parser['Settings']['Tamaño_Inicial'])
print(' [+]Creando población inicial')
poblacionInicial = init.generarPoblacionAleatoria(tamaño_inicial, flags)

#Creacion de directorio para jerarquía inicial
path_inicial = parser['Ajustes Pruebas']['Path_Inicio']
directorioBase = path_inicial + 'Ejecucion' + init.tiempo()
if not os.path.isdir(directorioBase):
    os.system('mkdir ' + directorioBase)
else:
    raise ValueError('\033[1;31m [!]Error, el archivo inicial ya existe.')

#Número de Generación
Gen = 0
#Poblacion actual
poblacion = poblacionInicial

#Programa a optimizar
programa = args.program

#Pesos de cada objetivo
Ram = float(parser['Settings']['Ram'])
Cpu = float(parser['Settings']['CPU'])
Peso = float(parser['Settings']['Peso'])
Rob = float(parser['Settings']['Robustez'])
Tiempo = float(parser['Settings']['Tiempo'])

#Tamaño población general
tamaño_general = int(parser['Settings']['Tamaño_General'])

#Máximo número de hilos concurrentes a la hora de ejecutar las pruebas
maximoNumeroHilos = int(parser['Ajustes Pruebas']['Threads'])

#Pesos de los objetivos
Ram = float(parser['Settings']['Ram'])
Cpu = float(parser['Settings']['CPU'])
Peso = float(parser['Settings']['Peso'])
Rob = float(parser['Settings']['Robustez'])
Tiempo = float(parser['Settings']['Tiempo'])

#Argumentos
Argumentos = args.arguments

#Ejecuciones para calcular robustez
ExecutionRobustness = int(parser['Ajustes Pruebas']['Ejecuciones_Robustez'])
#Pasar configuracion al archivo fitness
fitness.configuracion(maximoNumeroHilos, Ram, Cpu, Rob, Peso, Tiempo, Argumentos, ExecutionRobustness)

# Número de indibiduos a seleccionar
Select = int(parser['Settings']['A_Seleccionar'])

#Historico donde guardar una copia de la poblacion actual antes de pasar a la siguiente
historico = []
#Limite, indica el limite seleccionado
Limite = int(parser['Limites']['Limite'])
#Generacion máxima: 0
Max_Gen = int(parser['Limites']['Max_Gen'])
#Tiempo máximo de ejecución: 1
Max_Tiempo = int(parser['Limites']['Max_Tiempo'])
#Porcentage converjencia: 2
Convergencia = float(parser['Limites']['Convergencia'])
#Tiempo de inicio, para tener en cuenta en el Limite de Tiempo
tiempo_ini = time.time()

# Porcentaje de aleatorios en cada nueva Generación
aleatorios = float(parser['Settings']['Por_Aleatorios'])
#Cantidad máximo a mutar en cada indivduo generado en el crossover
radiacion = int(parser['Settings']['Radiacion'])

#Bucle donde se compila, testea, selecciona y se genera la siguiente generación,
#comprobando que no se cumplan los limites impuestos en conf.ini
while True:
    print(' [*]Compilando Generación ' + str(Gen))
    directorioGeneracionActual = auxiliar.compilarIndividuos(directorioBase, Gen, poblacion, programa)
    #Obtener puntuación de cada objetivo y actualizar objeto con puntuación
    print(' [+]Ejecutando pruebas Generación ' + str(Gen))
    fitness.test(poblacion, maximoNumeroHilos, directorioGeneracionActual)
    # Normalizar resultados entre 0 y 1
    if Ram:
        print(' [*]Normalizando Ram Generación ' + str(Gen))
        norm.normRam(poblacion)
    if Tiempo:
        print(' [*]Normalizando Tiempo Generación ' + str(Gen))
        norm.normTiempo(poblacion)
    if Peso:
        print(' [*]Normalizando Peso Generación ' + str(Gen))
        norm.normPeso(poblacion)
    if Rob:
        print(' [*]Normalizando Robustez Generación ' + str(Gen))
        norm.normRob(poblacion)
    if Cpu:
        print(' [*]Normalizando carga de la CPU Generación ' + str(Gen))
        norm.normCpu(poblacion)
    print(' [+]Obteniendo WSM Generación ' + str(Gen))
    # Ponderar los resultados según el peso
    norm.wsm(poblacion, Ram, Tiempo, Peso, Rob, Cpu)
    #Seleccionar
    print(' [*]Seleccionando individuos Generación ' + str(Gen))
    selected = auxiliar.selection(copy.deepcopy(poblacion), Select)
    #Fin generacion actual
    historico.append(copy.deepcopy(poblacion))
    if args.imprimir:
        auxiliar.imprimir(poblacion)
    #Comprobar limites para seguir o no
    print(' [+]Comprobando Límites')
    final = auxiliar.end(Limite, Max_Gen, Gen, Max_Tiempo, tiempo_ini, Convergencia, historico)
    if final:
        print(' [!]Saliendo... ')
        auxiliar.para_finalizar(historico, directorioBase, Ram, Tiempo, Peso, Rob, Cpu)
        sys.exit(0)
    #Preparaciones proxima generación
    Gen+=1
    #Crear nueva Poblacion
    print(' [*]Creando Generación ' + str(Gen))
    poblacion = cromosoma.siguienteGeneracion(selected, tamaño_general, aleatorios, radiacion, flags)