import os
import sys
import time
import signal
import random
import argparse
import threading
import subprocess
import configparser

sys.path.insert(1, './code')
from init import *
from operators import *
from selection import *
from pesos import *

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
###Variables globales
flags = []
population = []
parser = configparser.ConfigParser()
parser.read('conf.ini')
# Peso objetivos [Ram, Cpu, Peso, Rob, Tiempo]
Ram = float(parser['Settings']['Ram'])
Cpu = float(parser['Settings']['CPU'])
Peso = float(parser['Settings']['Peso'])
Rob = float(parser['Settings']['Robustez'])
Tiempo = float(parser['Settings']['Tiempo'])
# Ajustes tests
Executions = int(parser['Test']['Ejecuciones_Robustez'])
# tamaño población
Num_Pob = int(parser['Settings']['N_Poblacion'])
# path a archivo con flags elegidas
Path = parser['Flags']['Path']
# Número de hilos máximos
maxthreads = int(parser['Settings']['Threads'])
# directorio global
pathGlobal = ''
# archivo log global
logGlobal = ''
# Path generacion actual
pathGen = ''
# Path log generacion actual
logLocalGen = ''
# Número de Generación
Gen = 0
# Programa a optimizar y argumentos para que funcione si es necesario(se pasaran a los test)
Programa = args.program
Argumentos = args.arguments
# Vectores de Nx5 para guardar los resultados de los test [Ram, Cpu, Peso, Robustez, Tiempo]
# para no tomar en cuenta el valor lo ponemos a -1, valor que ningun test puede dar
resultRam = [-1.0] * Num_Pob
# para no tener que normalizar ponemos el peor valor ya
resultCpu = [1.0] * Num_Pob
resultTiempo = [-1.0] * Num_Pob
resultPeso = [-1.0] * Num_Pob
resultRob = [1.0] * Num_Pob
# Pool de hilos para asegurar el máximo de hilos a vez
pool = threading.Semaphore(value=maxthreads)
# Número de chromosomas a seleccionat
N_Select = int(parser['Limites']['N_Selecciones'])
if N_Select > Num_Pob:
    print('[!]Número de selecciones demasiado grande, debe ser menor o igual al tamaño de la población')
    exit(1)
if N_Select > Num_Pob:
    N_Select = Num_Pob
    # Crear población de tamaño N aleatoria
Por_Random = float(parser['Limites']['Por_Aleatorios'])
# Simboliza la cantidad de genomas que van a mutar en cada chromosoma
Radiacion = int(parser['Limites']['Radiacion'])
# Tipo de limite
Tipo = int(parser['Limites']['Limite'])
if Tipo == 0:
    Max_Gen = int(parser['Limites']['Max_Gen'])
elif Tipo == 1:
    Max_Tiempo = int(parser['Limites']['Max_Tiempo'])
elif Tipo == 3:
    Convergencia = int(parser['Limites']['Convergencia'])
else:
    print('[!]Tipo no existente, opciones: [0, 1, 2]')
    exit(1)


# Devuelve un string con el timestamp con el formato deseado

def tiempo():
    epoch = time.time()
    local = time.localtime(epoch)
    return '%d-%d-%d_%d:%d:%d' % (local.tm_mday, local.tm_mon, local.tm_year, local.tm_hour, local.tm_min, local.tm_sec)


# Función para obtener los pesos antes de normalizar


def test(chromosoma, N):
    pool.acquire()

    global resultRam, resultCpu, resultPeso, resultRob, resultTiempo
    logChromo = compilation(chromosoma, N, Programa)
    executable = pathGen + '/Chromo' + str(N) + '/Chromo' + str(N)
    resultChromo = []
    cantRam = -1.0  # para no tomar en cuenta el valor lo ponemos a -1, valor que ningun test puede dar
    cantCpu = 1.0  # para no tener que normalizar ponemos el peor valor ya
    cantPeso = -1.0
    cantRob = 1.0
    cantTiempo = -1.0

    if os.path.isfile(executable) and os.access(executable, os.X_OK):
        if Ram:
            cantRam = ram(executable, Argumentos).split('\n')
            cantRam = cantRam[0] or -1.0
            resultRam[N] = float(cantRam)
        if Cpu:
            cantCpu = cpuUse(executable, Argumentos).split('\n')
            cantCpu = cantCpu[0] or 1.0
            resultCpu[N] = float(cantCpu)
        if Peso:
            cantPeso = peso(executable, Argumentos).split('\n')
            cantPeso = cantPeso[0] or -1.0
            resultPeso[N] = float(cantPeso)
        if Rob:
            cantRob = robustness(executable, Argumentos, Executions).split('\n')
            if len(cantRob) > 1:
                cantRob = 1.0 - float(cantRob[0])
            else:
                cantRob = 1.0
            resultRob[N] = float(cantRob)
        if Tiempo:
            cantTiempo = exTime(executable, Argumentos) or -1.0
            resultTiempo[N] = float(cantTiempo)

    resultChromo = [cantRam, cantCpu, cantPeso, cantRob, cantTiempo]
    logChromo.write(
        '\n\nResultados pruebas\n\n\t' + str(resultChromo) + '\n')
    logChromo.close()

    pool.release()


def main():
    global Gen, Max_Gen, resultRam, resultCpu, resultPeso, resultRob, resultTiempo
    global population, pathGlobal, logGlobal, pathGen, logLocalGen
    file = open(Path, 'r').read().split('\n')
    for line in file:
        if line:
            flags.append(line)
    (pathGlobal, logGlobal) = inicializacionLog(
        Num_Pob, Ram, Tiempo, Cpu, Rob, Peso)
    population = createPop(Num_Pob, flags)
    for _ in range(Max_Gen):
        (pathGen, logLocalGen) = inicializaGen(Gen, Num_Pob)
        ini = tiempo()
        ini_t = time.time()
        logLocalGen.write('Tiempo de entrada: ' + str(ini) + '\n\n')
        print('[+]Compilación y pruebas Generación ' + str(Gen))
        threads = []
        try:
            for i in range(0, Num_Pob):
                threads.append(threading.Thread(
                    target=test, args=(population[i], i)))
            [t.start() for t in threads]
        except Exception as e:
            print('Excepción en hilo: ' + e)
        finally:
            [t.join() for t in threads]
        logLocalGen.write('Resultado Pruebas: \n\nRam:' + '\n\t' + str(resultRam) + '\n\nCarga CPU:' + '\n\t' + str(resultCpu) + '\n\nPeso:' +
                            '\n\t' + str(resultPeso) + '\n\nRobustez:' + '\n\t' + str(resultRob) + '\n\nTiempo de ejecución:' + '\n\t' + str(resultTiempo) + '\n\n')
        print('[+]Normalización Generación ' + str(Gen))
        normRam = normalizar(resultRam, Num_Pob)
        normCpu = resultCpu  # no normalizamos porque ya esta entre 0 y 1
        normPeso = normalizar(resultPeso, Num_Pob)
        normRob = resultRob
        normTiempo = normalizar(resultTiempo, Num_Pob)
        logLocalGen.write('Resultados tras normalizar: \n\nRam:' + '\n\t' + str(normRam) + '\n\nCarga CPU:' + '\n\t' + str(normCpu) + '\n\nPeso:' +
                            '\n\t' + str(normPeso) + '\n\nRobustez:' + '\n\t' + str(normRob) + '\n\nTiempo de ejecución:' + '\n\t' + str(normTiempo) + '\n\n')
        norm = [normRam, normCpu, normPeso, normRob, normTiempo]
        # WSM
        print('[+]WSM Generación ' + str(Gen))
        pesos = WSM(norm, Num_Pob, Ram, Cpu, Peso, Rob, Tiempo)
        logLocalGen.write('Resultados tras WSM: \n\t' + str(pesos) + '\n\n')
        # Selection
        print('[+]Selección Generación ' + str(Gen))
        (selectionIndex, selected) = selection(pesos, N_Select)
        logLocalGen.write('Indices y datos seleccionados: \n\n\t ( ' + str(selectionIndex) +
                            ', ' + str(selected) + ' )\n\n')
        # generacion de poblacion siguiente (mutacion y aleatorios)
        population = generarDescendientes(selectionIndex, population, Num_Pob, N_Select, Por_Random, flags, Radiacion)
        # Fin de Generacion:
        fin = tiempo()
        fin_t = time.time()
        logLocalGen.write('Tiempo de salida: ' + str(fin) +
                            '\n\nDuración: ' + str(fin_t - ini_t) + '\n\n')
        Gen += 1
        resultRam = [-1.0] * Num_Pob
        resultCpu = [1.0] * Num_Pob
        resultTiempo = [-1.0] * Num_Pob
        resultPeso = [-1.0] * Num_Pob
        resultRob = [1.0] * Num_Pob
        # Cambio de Generacion y analisis de si cambia
    print(selected)


if __name__ == "__main__":
    main()

logGlobal.close()
logLocalGen.close()