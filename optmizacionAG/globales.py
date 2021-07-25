""" Este archivo contiene la mayoría de
    declaraciones e inicializaciones de las
    variables globales
"""

import argparse
import configparser
import os
import sys
import time

sys.path.insert(1, "./code")
import init


"""Archivo de configuración"""
parser = configparser.ConfigParser()
parser.read("conf.ini")

""" Argumentos de programa """
# Declaración de argumentos de  programa
argparser = argparse.ArgumentParser()
argparser.add_argument(
    "-p", "--programa", dest="program", help="Path absoluto del programa a optimizar"
)
argparser.add_argument(
    "-a",
    "--arguments",
    dest="arguments",
    help="Argumentos del programa para hacer pruebas",
)
argparser.add_argument(
    "-i", "--imprimir", dest="imprimir", default=False, action="store_true"
)
argparser.add_argument(
    "-dF", "--debugFlags", dest="debug", default=False, action="store_true"
)
args = argparser.parse_args()
# Programa a optimizar
programa = args.program
# Argumentos del programa a optimizar
Argumentos = args.arguments
# Salida de errores al compilar
debug = args.debug

"""Variables Globales"""

# Path inicial para salida
path_inicial = parser["Ajustes Pruebas"]["Path_Inicio"]
# Directorio para la salida
directorioBase = path_inicial + "Ejecucion" + init.tiempo()
# Creación del directorio
if not os.path.isdir(directorioBase):
    os.system("mkdir " + directorioBase)
else:
    raise ValueError("\033[1;31m [!]Error, el archivo inicial ya existe.")

# Archivo con flags para optimización
path = parser["Flags"]["Path"]

# Tamaño inicial de la población
tamaño_inicial = int(parser["Settings"]["Tamaño_Inicial"])

# Número de Generación
Gen = 0

# Flags dependientes del programa
flagsDependencias = str(parser["Flags"]["Flags Dependencias"])
# Path programas dependientes del programa a optimizar
dependencias = str(parser["Flags"]["Dependencias"])

# Pesos de cada objetivo
Ram = float(parser["Settings"]["Ram"])
Cpu = float(parser["Settings"]["CPU"])
Peso = float(parser["Settings"]["Peso"])
Rob = float(parser["Settings"]["Robustez"])
Tiempo = float(parser["Settings"]["Tiempo"])
# Ejecuciones para calcular robustez
ExecutionRobustness = int(parser["Ajustes Pruebas"]["Ejecuciones_Robustez"])

# Tamaño población
tamaño_general = int(parser["Settings"]["Tamaño_General"])

# Máximo número de hilos concurrentes
maximoNumeroHilos = int(parser["Ajustes Pruebas"]["Threads"])

# Número de individuos a seleccionar
Select = int(parser["Settings"]["A_Seleccionar"])

# Historico de individuos
historico = []

# Limite conigurado
Limite = int(parser["Limites"]["Limite"])
# Generacion máxima
Max_Gen = int(parser["Limites"]["Max_Gen"])
# Tiempo máximo de ejecución
Max_Tiempo = int(parser["Limites"]["Max_Tiempo"])
# Tiempo de inicio, para tener en cuenta en el Limite de Tiempo
tiempo_ini = time.time()
# Generación mínima
Generacion_convergencia = int(parser["Limites"]["Generacion_Convergencia"])

# Porcentaje de aleatorios en cada nueva Generación
aleatorios = float(parser["Settings"]["Por_Aleatorios"])
# Cantidad máximo a mutar en cada indivduo generado en el crossover
radiacion = int(parser["Settings"]["Radiacion"])
