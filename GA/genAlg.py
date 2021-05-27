import os
import sys
import time
import signal
import random
import argparse
import threading
import subprocess
import configparser


def signal_handler(sig, frame):
    print('\n[!]Saliendo...')
    os._exit(1)


signal.signal(signal.SIGINT, signal_handler)

"""
    Declaracion de variables globales
"""
argparser = argparse.ArgumentParser()
argparser.add_argument("-p", "--program", dest = "program", help="Program to optimize")
argparser.add_argument("-a", "--arguments",dest = "arguments", help="Arguments for the program to work")
args = argparser.parse_args()
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
# Tiempo inicial
timestamp = ''
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
# Límites
Max_Gen = int(parser['Limites']['Max_Gen'])
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
    N_Select = Num_Pob
    # Crear población de tamaño N aleatoria
Por_Random = float(parser['Limites']['Por_Aleatorios'])
#Simboliza la cantidad de genomas que van a mutar en cada chromosoma
Radiacion = int(parser['Limites']['Radiacion'])

def createPop(N):
    global population
    population = []
    for i in range(0, N):
        cromo = []
        for flag in flags:
            tupla = (random.randint(0, 1), flag)
            cromo.append(tupla)
        population.append(cromo)
# Devuelve un string con el timestamp de la forma deseada


def tiempo():
    epoch = time.time()
    local = time.localtime(epoch)
    return '%d.%d.%d.%d.%d.%d' % (local.tm_mday, local.tm_mon, local.tm_year, local.tm_hour, local.tm_min, local.tm_sec)

# Inicialización y creación de la estructura para logging


def inicializacionLog():
    global timestamp, pathGlobal, logGlobal
    timestamp = tiempo()
    print('Execution started at ' + timestamp)
    os.system('mkdir /tmp/algorithmExecution'+timestamp)
    pathGlobal = '/tmp/algorithmExecution'+timestamp
    pathGlobalFile = '/tmp/algorithmExecution'+timestamp+'/logGlobal.txt'
    os.system('touch ' + pathGlobalFile)
    logGlobal = open(pathGlobalFile, 'a')
    logGlobal.write('Execution started in ' + timestamp + '\n')
    logGlobal.write('Population Size: ' + str(Num_Pob) + '\n')
    logGlobal.write('Weight: ' + '\n')
    logGlobal.write('\tRam: ' + str(Ram) + '\n')
    logGlobal.write('\tTime: ' + str(Tiempo) + '\n')
    logGlobal.write('\tCpu load: ' + str(Cpu) + '\n')
    logGlobal.write('\tRobustness: ' + str(Rob) + '\n')
    logGlobal.write('\tBinary Weigth: ' + str(Peso) + '\n')
    logGlobal.write('\nFlags:\n')
    logGlobal.write('\t' + str(flags) + '\n')

# Inicialización de archivos para cada Generación de individuos


def inicializaGen(N, pob):
    global pathGen, logLocalGen
    pathGen = pathGlobal + '/Gen' + str(N)
    os.system('mkdir ' + pathGen)
    pathLocalFile = pathGen + '/localFileGen' + str(N)
    os.system('touch ' + pathLocalFile)
    logLocalGen = open(pathLocalFile, 'a')
    timestamp = tiempo()
    logLocalGen.write('Generation start: ' + timestamp + '\n')
    for ind in range(0, pob):
        pathChromo = pathGen + '/Chromo' + str(ind)
        os.system('mkdir ' + pathChromo)
        os.system('touch ' + pathChromo + '/log' +
                  'Gen' + str(N) + '_Ind' + str(ind))

# Ejecución de comandos con vuelta de outpur y errores


def executionWithOutput(command):
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    return (result.stdout, result.stderr)

# Compilación de programa y loggeo


def compilation(chromosoma, N):
    pathChromo = pathGen + '/Chromo' + str(N)
    logChromo = pathGen + '/Chromo' + \
        str(N) + '/logGen' + str(Gen) + '_Ind' + str(N)
    log = open(logChromo, 'a')
    log.write('Executed at ' + tiempo() + '\n')
    log.write('Chromosoma: \n')
    log.write('\t' + str(chromosoma) + '\n')
    line = ''
    for flag in chromosoma:
        if flag[0]:
            line += flag[1] + ' '
    line = 'gcc ' + Programa + ' -o ' + \
        pathChromo + '/Chromo' + str(N) + ' ' + line
    log.write('Compilation line: \n')
    log.write('\t' + line + '\n')
    log.write('Output after compiling: \n\t')
    (out, err) = executionWithOutput(line)
    log.write(out + '\n')
    log.write('Error after compiling: \n\t')
    log.write(err + '\n')
    return log

# Uso de ram


def ram(executable):
    if Argumentos:
        (out, err) = executionWithOutput("./test/ram.sh -b \'" + executable + " " + Argumentos + "\'")
    else:
        (out, err) = executionWithOutput("./test/ram.sh -b " + executable)
    return out

# Uso de CPU


def cpuUse(executable):
    if Argumentos:
        (out, err) = executionWithOutput('./test/cpu.sh -b \'' + executable + " " + Argumentos + "\'" + ' -t 1')
    else:
        (out, err) = executionWithOutput('./test/cpu.sh -b ' + executable + ' -t 1')
    return out

# Peso del binario


def peso(executable):
    (out, err) = executionWithOutput('./test/peso.sh ' + executable)
    return out

# Robustez del binario


def robustness(executable):
    if Argumentos:
        (out, err) = executionWithOutput(
            './test/robustez.sh -b ' + executable + ' -e ' + str(Executions) +' -a \'' + Argumentos + '\'')
    else:
        (out, err) = executionWithOutput(
            './test/robustez.sh -b ' + executable + ' -e ' + str(Executions))
    return out

# Tiempo de ejecución


def exTime(executable):
    if Argumentos:
        (out, err) = executionWithOutput('./test/tiempo.sh \'' + executable + " " + Argumentos + "\'")
    else:
        (out, err) = executionWithOutput('./test/tiempo.sh ' + executable)
    numero = err.split(',')  # Time usa stderr para la salida
    out = float(numero[0] + '.' + numero[1])
    return out

# Función para obtener los pesos antes de normalizar


def test(chromosoma, N):
    pool.acquire()

    global resultRam, resultCpu, resultPeso, resultRob, resultTiempo
    logChromo = compilation(chromosoma, N)
    executable = pathGen + '/Chromo' + str(N) + '/Chromo' + str(N)
    resultChromo = []
    cantRam = -1.0  # para no tomar en cuenta el valor lo ponemos a -1, valor que ningun test puede dar
    cantCpu = 1.0  # para no tener que normalizar ponemos el peor valor ya
    cantPeso = -1.0
    cantRob = 1.0
    cantTiempo = -1.0

    if os.path.isfile(executable) and os.access(executable, os.X_OK):
        if Ram:
            cantRam = ram(executable).split('\n')
            # !! revisar esta forma de quitar salto de linea
            cantRam = cantRam[0] or -1.0
            resultRam[N] = float(cantRam)
        if Cpu:
            cantCpu = cpuUse(executable).split('\n')
            cantCpu = cantCpu[0] or 1.0
            resultCpu[N] = float(cantCpu)
        if Peso:
            cantPeso = peso(executable).split('\n')
            cantPeso = cantPeso[0] or -1.0
            resultPeso[N] = float(cantPeso)
        if Rob:
            cantRob = robustness(executable).split('\n')
            if len(cantRob) > 1:
                # probablemente varíe
                #cantRob = 1.0 - (float(cantRob[0]) + float(cantRob[1]))
                cantRob = 1.0 - float(cantRob[0])
            else:
                cantRob = 1.0

            resultRob[N] = float(cantRob)

        if Tiempo:
            cantTiempo = exTime(executable) or -1.0
            resultTiempo[N] = float(cantTiempo)

    resultChromo = [cantRam, cantCpu, cantPeso, cantRob, cantTiempo]
    logChromo.write('\n\nResultados pruebas[Ram, Cpu, Peso, Rob, Tiempo]:\n\n\t' + str(resultChromo) + '\n')
    logChromo.close()

    pool.release()

# Normalizar pesos


def normalizar(vector, N):  # revisar
    # buscando maximos y minimos
    max = 0.0
    min = float('inf')  # revisar
    for j in range(0, N):

        if min > vector[j] and not(vector[j] < 0):
            min = vector[j]
        if max < vector[j] and not(vector[j] < 0):
            max = vector[j]

    if (max - min) == 0.0:
        return [1.0]*N

    for j in range(0, N):
        if vector[j] < 0:
            vector[j] = 1.0
        else:
            vector[j] = (vector[j] - min) / (max - min)

    return vector

# WSM


def WSM(matrix, N):
    result = []
    for i in range(0, N - 1):
        wsm = matrix[0][i]*Ram + matrix[1][i]*Cpu + matrix[2][i] * \
            Peso + matrix[3][i]*Rob + matrix[4][i]*Tiempo
        result.append(wsm)
    return result

# Selection function


def selection(vector, to_select):
    sorted_vector = sorted(vector)
    selected_index = []
    for N in range(to_select):
        index = vector.index(sorted_vector[N])
        selected_index.append(index)
        vector[index] = None
    return (sorted(selected_index), sorted_vector[:to_select])


def generarDescendientes(population, selectionIndex, Num_Pob, Radiacion):
    '''
    print(selectionIndex)
    selected = []
    binaryFlags = [None]*len(selectionIndex)
    for i in selectionIndex:
        selected.append(population[i])
        for i in range(len(selectionIndex)-1):

            binaryFlags.insert(i, selected[i])

    print(binaryFlags)
    '''
    return population

def main():
    global Gen, Max_Gen, resultRam, resultCpu, resultPeso, resultRob, resultTiempo, population
    file = open(Path, 'r').read().split('\n')
    for line in file:
        if line:
            flags.append(line)
    inicializacionLog()
    createPop(Num_Pob)
    # para bucle de generaciones
    # De momento solo hay este límite, podría implementar ( tiempo, genercion, convergencia )
    for _ in range(Max_Gen):
        inicializaGen(Gen, Num_Pob)
        ini = tiempo()
        ini_t = time.time()
        logLocalGen.write('Tiempo de entrada: ' + str(ini) + '\n\n')
        print('[+]Compilation and test Generation ' + str(Gen))
        threads = []
        try:
            for i in range(0, Num_Pob):
                threads.append(threading.Thread(
                    target=test, args=(population[i], i)))
            [t.start() for t in threads]
        except Exception as e:
            print('Exception in threading: ' + e)
        finally:
            [t.join() for t in threads]
        logLocalGen.write('Test results: \n\nRam:' + '\n\t' + str(resultRam) + '\n\nCpu:' + '\n\t' + str(resultCpu) + '\n\nPeso:' +
                            '\n\t' + str(resultPeso) + '\n\nRobustez:' + '\n\t' + str(resultRob) + '\n\nTiempo:' + '\n\t' + str(resultTiempo) + '\n\n')
        print('[+]Normalization Generation ' + str(Gen))
        normRam = normalizar(resultRam, Num_Pob)
        normCpu = resultCpu  # no normalizamos porque ya esta entre 0 y 1
        normPeso = normalizar(resultPeso, Num_Pob)
        normRob = resultRob
        normTiempo = normalizar(resultTiempo, Num_Pob)
        logLocalGen.write('Normalization results: \n\nRam:' + '\n\t' + str(normRam) + '\n\nCpu:' + '\n\t' + str(normCpu) + '\n\nPeso:' +
                            '\n\t' + str(normPeso) + '\n\nRobustez:' + '\n\t' + str(normRob) + '\n\nTiempo:' + '\n\t' + str(normTiempo) + '\n\n')
        norm = [normRam, normCpu, normPeso, normRob, normTiempo]
        # WSM
        print('[+]WSM Generation ' + str(Gen))
        pesos = WSM(norm, Num_Pob)
        logLocalGen.write('WSM results: \n\t' + str(pesos) + '\n\n')
        # Selection
        print('[+]Selection Generation ' + str(Gen))
        (selectionIndex, selected) = selection(pesos, N_Select)
        logLocalGen.write('Selected index and data: \n\n\t ( ' + str(selectionIndex) +
                            ', ' + str(selected) + ' )\n\n')
        # generacion de poblacion siguiente (mutacion y aleatorios)
        population = generarDescendientes(population, selectionIndex, Num_Pob, Radiacion)
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


if __name__ == "__main__":
    main()

logGlobal.close()
logLocalGen.close()