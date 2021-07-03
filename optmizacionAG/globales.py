import configparser
import time
import sys
import os
import argparse
sys.path.insert(1, './code')
import init

parser = configparser.ConfigParser()
parser.read('conf.ini')

#Argumentos de programa
argparser = argparse.ArgumentParser()
argparser.add_argument("-p", "--programa", dest="program",
                        help="Path absoluto del programa a optimizar")
argparser.add_argument("-a", "--arguments", dest="arguments",
                        help="Argumentos del programa para hacer pruebas")
argparser.add_argument('-i', "--imprimir", dest="imprimir", default=False, action='store_true')
argparser.add_argument('-dF', "--debugFlags", dest="debug", default=False, action='store_true')
args = argparser.parse_args()
#Programa a optimizar
programa = args.program
#Argumentos
Argumentos = args.arguments
#Activar salida de errores al compilar o no
debug = args.debug

#Creacion de directorio para jerarquía inicial
path_inicial = parser['Ajustes Pruebas']['Path_Inicio']
directorioBase = path_inicial + 'Ejecucion' + init.tiempo()
if not os.path.isdir(directorioBase):
    os.system('mkdir ' + directorioBase)
else:
    raise ValueError('\033[1;31m [!]Error, el archivo inicial ya existe.')

#Leer e inicializar objetis Flag
path = parser['Flags']['Path']

#Crear poblacion inicial aleatoria con tamaño indicado en el archivo de configuracion
tamaño_inicial = int(parser['Settings']['Tamaño_Inicial'])

#Número de Generación
Gen = 0

#Flags necesarias para las dependencias del programa
flagsDependencias = str(parser['Flags']['Flags Dependencias'])
#Path archivos de programas necesarios para compilar
dependencias = str(parser['Flags']['Dependencias'])

#Pesos de cada objetivo
Ram = float(parser['Settings']['Ram'])
Cpu = float(parser['Settings']['CPU'])
Peso = float(parser['Settings']['Peso'])
Rob = float(parser['Settings']['Robustez'])
Tiempo = float(parser['Settings']['Tiempo'])
#Ejecuciones para calcular robustez
ExecutionRobustness = int(parser['Ajustes Pruebas']['Ejecuciones_Robustez'])

#Tamaño población general
tamaño_general = int(parser['Settings']['Tamaño_General'])

#Máximo número de hilos concurrentes a la hora de ejecutar las pruebas
maximoNumeroHilos = int(parser['Ajustes Pruebas']['Threads'])

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
#Tiempo de inicio, para tener en cuenta en el Limite de Tiempo
tiempo_ini = time.time()

# Porcentaje de aleatorios en cada nueva Generación
aleatorios = float(parser['Settings']['Por_Aleatorios'])
#Cantidad máximo a mutar en cada indivduo generado en el crossover
radiacion = int(parser['Settings']['Radiacion'])

# Generación mínima para comprobar la convergencia
Generacion_convergencia = int(parser['Limites']['Generacion_Convergencia'])