import os
import sys
import time
import signal
import random
import threading
import subprocess
import configparser


def signal_handler(sig, frame):
    print('\n[!]Saliendo...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

"""
    Declaracion de variables globales
"""

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
# Programa a optimizar
Programa = sys.argv[1]
# Matriz de Nx5 para guardar los resultados de los test [Ram, Cpu, Peso, Robustez, Tiempo]
result = [None] * Num_Pob
# Pool de hilos para asegurar el máximo de hilos a vez
pool = threading.Semaphore(value=maxthreads)

# Crear población de tamaño N aleatoria


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
    log.close()

# Uso de ram


def ram(executable):
    (out, err) = executionWithOutput('./test/ram.sh -b ' + executable)
    return out

# Uso de CPU


def cpuUse(executable):
    (out, err) = executionWithOutput('./test/cpu.sh -b ' + executable + ' -t 1')
    return out

# Peso del binario


def peso(executable):
    (out, err) = executionWithOutput('./test/peso.sh ' + executable)
    return out

# Robustez del binario


def robustness(executable):
    (out, err) = executionWithOutput(
        './test/robustez.sh -b ' + executable + ' -e ' + str(Executions))
    return out

# Tiempo de ejecución


def exTime(executable):
    (out, err) = executionWithOutput('./test/tiempo.sh ' + executable)
    numero = err.split(',')  # Time usa stderr para la salida
    out = float(numero[0] + '.' + numero[1])
    return out

# Función para obtener los pesos antes de normalizar


def test(chromosoma, N):
    pool.acquire()

    global result
    compilation(chromosoma, N)
    executable = pathGen + '/Chromo' + str(N) + '/Chromo' + str(N)
    cantRam = 1.0
    cantCpu = 1.0
    cantPeso = 1.0
    cantRob = 1.0
    cantTiempo = 1.0
    if os.path.isfile(executable) and os.access(executable, os.X_OK):
        if Ram:
            cantRam = ram(executable).split('\n')
            # !! revisar esta forma de quitar salto de linea
            cantRam = cantRam[0] or 1.0
        if Cpu:
            cantCpu = cpuUse(executable).split('\n')
            cantCpu = cantCpu[0] or 1.0
        if Peso:
            cantPeso = peso(executable).split('\n')
            cantPeso = cantPeso[0] or 1.0
        if Rob:
            cantRob = robustness(executable).split('\n')
            if len(cantRob) > 1:
                cantRob = 1.0 - (float(cantRob[0]) + float(cantRob[1]))  # probablemente varíe
            else:
                cantRob = 1.0
        if Tiempo:
            cantTiempo = exTime(executable) or 1.0

        result[N] = [float(cantRam), float(cantCpu), float(cantPeso), cantRob, float(cantTiempo)]

    else:
        result[N] = [1.0, 1.0, 1.0, 1.0, 1.0]

    pool.release()

# Normalizar pesos


def normalizar(matrix, N): #revisar
    # buscando maximos y minimos
    for i in range(5):
        max = 0.0
        min = float('inf') #revisar
        for j in range(N):
            if matrix[i][j] == 1.0 :
                break;
            if min > matrix[i][j]:
                min = matrix[i][j]
            if max < matrix[i][j]:
                max = matrix[i][j]

        print(max)
        print(min)
        if (max - min) == 0.0:
            break

        for j in range(N):
            print(matrix[i][j])
            matrix[i][j] = (matrix[i][j] - min) / (max - min)
            print(matrix[i][j])
    return matrix

# Main


def main():
    global Gen, Max_Gen, result
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
        logLocalGen.write('Tiempo de entrada: ' + str(ini) + '\n')
        print('[+]Compilation and test Generation ' + str(Gen))
        threads = []
        try:
            for i in range(0, len(population)):
                threads.append(threading.Thread(
                    target=test, args=(population[i], i)))
            [t.start() for t in threads]
        except Exception as e:
            print('Exception in threading: ' + e)
        finally:
            [t.join() for t in threads]
        Gen += 1
        logLocalGen.write('Test results: \n')
        logLocalGen.write('\t' + str(result) + '\n')
        resultAfterNorm = normalizar(result, Num_Pob)
        logLocalGen.write('Normalization results: \n')
        logLocalGen.write('\t' + str(resultAfterNorm) + '\n')
        print(str(resultAfterNorm))
        # WSM
        # Fin de Generacion:
        fin = tiempo()
        fin_t = time.time()
        logLocalGen.write('Tiempo de salida: ' + str(fin) + '\n')
        logLocalGen.write('Duración: ' + str(fin_t - ini_t) + '\n')
        result = [None] * Num_Pob
        createPop(Num_Pob)  # Sustituir por eleccion/mutacion/descendientes
        # Cambio de Generacion


if __name__ == "__main__":
    main()

logGlobal.close()
logLocalGen.close()
