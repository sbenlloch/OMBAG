import configparser
import subprocess
import threading
import time
import os

maximoNumeroHilos = 2
pesoRam = 0
pesoCpu = 0
pesoRob = 0
pesoPeso = 0
pesoTiempo = 0
Argumentos = ''
ExecutionRobustness = 97

def configuracion(NumeroHilos, Ram, Cpu, Rob, Peso, Tiempo, Args, ExRob):
    global maximoNumeroHilos, pesoRam, pesoCpu, pesoRob, pesoPeso, pesoTiempo, Argumentos, ExecutionRobustness
    maximoNumeroHilos = NumeroHilos
    pesoRam = Ram
    pesoCpu = Cpu
    pesoRob = Rob
    pesoPeso = Peso
    pesoTiempo = Tiempo
    Argumentos = Args
    ExecutionRobustness = ExRob


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
    if Argumentos:
        (out, err) = executionWithOutput(
            './test/tiempo.sh \'' + executable + " " + Argumentos + "\'")
    else:
        (out, err) = executionWithOutput('./test/tiempo.sh ' + executable)
    numero = err.split(',')  # Time usa stderr para la salida
    out = float(numero[0] + '.' + numero[1])
    archivoTiempo = open(directorioActual + 'Tiempo.txt', 'a')
    archivoTiempo.write('Salida: ' + str(out))
    archivoTiempo.close()
    return out


def pruebas(cromosoma, i, pathActual):
    pool.acquire()
    directorioActual = pathActual + '/Cromosoma' + str(i) +  '/'
    executable = directorioActual + 'Cromosoma' + str(i)
    if os.path.isfile(executable) and os.access(executable, os.X_OK):
        if pesoRam:
            cantRam = ram(executable, Argumentos, directorioActual).split('\n')
            cantRam = cantRam[0] or -1.0
            cromosoma.resultRam = float(cantRam)

        if pesoCpu:
            cantCpu = cpuUse(executable, Argumentos, directorioActual).split('\n')
            cantCpu = cantCpu[0] or 1.1
            cromosoma.resultCPU = float(cantCpu)

        if pesoPeso:
            cantPeso = peso(executable, Argumentos, directorioActual).split('\n')
            cantPeso = cantPeso[0] or -1.0
            cromosoma.resultPeso = float(cantPeso)

        if pesoRob:
            cantRob = robustness(executable, Argumentos, ExecutionRobustness, directorioActual).split('\n')
            if len(cantRob) > 1:
                cantRob = 1.0 - float(cantRob[0])
            else:
                cantRob = 1.1
            cromosoma.resultRob = float(cantRob)

        if pesoTiempo:
            cantTiempo = exTime(executable, Argumentos, directorioActual) or -1.0
            cromosoma.resultTiempo = float(cantTiempo)

    pool.release()


def test(poblacion, maximoNumeroHilos, directorioGeneracionActual):
    threads = []
    try:
        for i in range(len(poblacion)):
            threads.append(threading.Thread(
                target=pruebas, args=(poblacion[i], i, directorioGeneracionActual)))
        [t.start() for t in threads]
    except Exception as e:
        print('Excepción en hilos: ' + str(e))
    finally:
        [t.join() for t in threads]