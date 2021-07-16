import os
import subprocess
import threading
import time

from globales import *

# Pool de hilos para asegurar el máximo número de hilos a la vez
pool = threading.Semaphore(value=maximoNumeroHilos)


def executionWithOutput(command):
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    return (result.stdout, result.stderr)


# Uso de ram
def ram(executable, Argumentos, directorioActual):
    if Argumentos:
        (out, err) = executionWithOutput(
            "./test/ram.sh -b " + executable + " -a \'" + Argumentos + "\'")
    else:
        (out, err) = executionWithOutput("./test/ram.sh -b " + executable)
    archivoRAM = open(directorioActual + 'RAM.txt', 'a')
    archivoRAM.write('Salida: ' + out + '\nError: ' + err)
    archivoRAM.close()
    return out


# Uso de CPU
def cpuUse(executable, Argumentos, directorioActual):
    if Argumentos:
        (out, err) = executionWithOutput('./test/cpu.sh -b ' +
                                         executable + " -a \'" + Argumentos + "\'" + ' -t 1')
    else:
        (out, err) = executionWithOutput(
            './test/cpu.sh -b ' + executable + ' -t 1')
    archivoCPU = open(directorioActual + 'CPU.txt', 'a')
    archivoCPU.write('Salida: ' + out + '\nError: ' + err)
    archivoCPU.close()
    return out


# Peso del binario
def peso(executable, Argumentos, directorioActual):
    (out, err) = executionWithOutput('./test/peso.sh ' + executable)
    archivoPeso = open(directorioActual + 'Peso.txt', 'a')
    archivoPeso.write('Salida: ' + out + '\nError: ' + err)
    archivoPeso.close()
    return out


# Robustez del binario
def robustness(executable, Argumentos, Executions, directorioActual):
    if Argumentos:
        (out, err) = executionWithOutput(
            './test/robustez.sh -b ' + executable + ' -e ' + str(Executions) + ' -a \'' + Argumentos + '\'')
    else:
        (out, err) = executionWithOutput(
            './test/robustez.sh -b ' + executable + ' -e ' + str(Executions))
    archivoRobustez = open(directorioActual + 'Robustez.txt', 'a')
    archivoRobustez.write('Salida: ' + out + '\nError: ' + err)
    archivoRobustez.close()
    return out


# Tiempo de ejecución
def exTime(executable, Argumentos, directorioActual):
    (out, err) = executionWithOutput('./test/tiempo.sh -b ' + executable + " -a " + Argumentos + " -e 1")
    if '.' in out:
        archivoTiempo = open(directorioActual + 'Tiempo.txt', 'a')
        archivoTiempo.write('Salida: ' + str(out))
        archivoTiempo.close()
        return out
    numero = out.split(',')
    salida = float(numero[0] + '.' + numero[1])
    archivoTiempo = open(directorioActual + 'Tiempo.txt', 'a')
    archivoTiempo.write('Salida: ' + str(salida))
    archivoTiempo.close()
    return salida


def pruebas(cromosoma, i, pathActual):
    pool.acquire()
    directorioActual = pathActual + '/Cromosoma' + str(i) + '/'
    executable = directorioActual + 'Cromosoma' + str(i)
    if os.path.isfile(executable) and os.access(executable, os.X_OK):
        if Ram:
            cantRam = ram(executable, Argumentos, directorioActual).split('\n')
            cantRam = cantRam[0] or -1.0
            cromosoma.resultRam = float(cantRam)

        if Cpu:
            cantCpu = cpuUse(executable, Argumentos,
                                directorioActual).split('\n')
            cantCpu = cantCpu[0] or -1.0
            cromosoma.resultCPU = float(cantCpu)

        if Peso:
            cantPeso = peso(executable, Argumentos,
                            directorioActual).split('\n')
            cantPeso = cantPeso[0] or -1.0
            cromosoma.resultPeso = float(cantPeso)

        if Rob:
            cantRob = robustness(
                executable, Argumentos, ExecutionRobustness, directorioActual).split('\n')
            if len(cantRob) > 1:
                cantRob = 1.0 - float(cantRob[0])
            else:
                cantRob = -1.0
            cromosoma.resultRob = float(cantRob)

        if Tiempo:
            cantTiempo = exTime(executable, Argumentos,
                                directorioActual) or -1.0
            cromosoma.resultTiempo = float(cantTiempo)

    pool.release()



def test(poblacion, maximoNumeroHilos, directorioGeneracionActual):
    threads = []
    try:

        for i in range(len(poblacion)):

            if not poblacion[i].pruebasHechas:
                threads.append(threading.Thread(
                    target=pruebas, args=(poblacion[i], i, directorioGeneracionActual)))
                poblacion[i].pruebasHechas = True

        [t.start() for t in threads]
    except Exception as e:
        print('Excepción en hilos: ' + str(e))
    finally:
        [t.join() for t in threads]
