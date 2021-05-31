import os
import sys
import time
import signal
import random
import subprocess

pathGlobal = ''
pathGen = ''
Gen = 0
flags = []


def signal_handler(sig, frame):
    print('\n[!]Saliendo...')
    os._exit(1)


signal.signal(signal.SIGINT, signal_handler)

# Función para crear población inicial aleatoria, recibe el tamaño de la población


def createPop(N, list_flags):
    global flags
    flags = list_flags
    population = []
    for i in range(0, N):
        cromo = []
        for flag in flags:
            tupla = (random.randint(0, 1), flag)
            cromo.append(tupla)
        population.append(cromo)
    return population

# Devuelve un string con el timestamp con el formato deseado


def tiempo():
    epoch = time.time()
    local = time.localtime(epoch)
    return '%d-%d-%d_%d:%d:%d' % (local.tm_mday, local.tm_mon, local.tm_year, local.tm_hour, local.tm_min, local.tm_sec)

# Inicialización y creación de la estructura para logging


def inicializacionLog(Num_Pob, Ram, Tiempo, Cpu, Rob, Peso):
    global pathGlobal, logGlobal
    timestamp = tiempo()
    print('Ejecución iniciada en ' + timestamp)
    os.system('mkdir /tmp/algorithmExecution'+timestamp)
    pathGlobal = '/tmp/algorithmExecution'+timestamp
    pathGlobalFile = '/tmp/algorithmExecution'+timestamp+'/logGlobal.txt'
    os.system('touch ' + pathGlobalFile)
    logGlobal = open(pathGlobalFile, 'a')
    logGlobal.write('Ejecución iniciada en ' + timestamp + '\n')
    logGlobal.write('Tamaño de la población: ' + str(Num_Pob) + '\n')
    logGlobal.write('Pesos dados: ' + '\n')
    logGlobal.write('\tRam: ' + str(Ram) + '\n')
    logGlobal.write('\tTiempo: ' + str(Tiempo) + '\n')
    logGlobal.write('\tCarga de la CPU: ' + str(Cpu) + '\n')
    logGlobal.write('\tRobustez: ' + str(Rob) + '\n')
    logGlobal.write('\tPeso del binario: ' + str(Peso) + '\n')
    logGlobal.write('\nFlags:\n\t' + str(flags) + '\n')
    return (pathGlobal, logGlobal)

# Inicialización de archivos para cada Generación de individuos


def inicializaGen(N, pob):
    global pathGen, Gen
    Gen = N
    pathGen = pathGlobal + '/Gen' + str(N)
    os.system('mkdir ' + pathGen)
    pathLocalFile = pathGen + '/localFileGen' + str(N)
    os.system('touch ' + pathLocalFile)
    logLocalGen = open(pathLocalFile, 'a')
    timestamp = tiempo()
    logLocalGen.write(
        'Ejecución de la Generación actual a ' + timestamp + '\n')
    for ind in range(0, pob):
        pathChromo = pathGen + '/Chromo' + str(ind)
        os.system('mkdir ' + pathChromo)
        os.system('touch ' + pathChromo + '/log' +
                  'Gen' + str(N) + '_Ind' + str(ind))
    return (pathGen, logLocalGen)

# Ejecución de comandos con vuelta de output y errores


def executionWithOutput(command):
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    return (result.stdout, result.stderr)

# Compilación de programa y salida en archivo local individuo


def compilation(chromosoma, N, Programa):
    pathChromo = pathGen + '/Chromo' + str(N)
    logChromo = pathGen + '/Chromo' + \
        str(N) + '/logGen' + str(Gen) + '_Ind' + str(N)
    log = open(logChromo, 'a')
    log.write('Ejecutado a ' + tiempo() + '\n')
    log.write('Cromosoma: \n\t' + str(chromosoma) + '\n')
    line = ''
    for flag in chromosoma:
        if flag[0]:
            line += flag[1] + ' '
    line = 'gcc ' + Programa + ' -o ' + \
        pathChromo + '/Chromo' + str(N) + ' ' + line
    log.write('Línea de compilación: \n\t' + line + '\n')
    (out, err) = executionWithOutput(line)
    log.write('Salida de la compilación: \n\t' + out +
              '\nError en compilación: \n\t' + err + '\n')
    return log