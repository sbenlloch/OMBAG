import subprocess
import signal
import os

def signal_handler(sig, frame):
    print('\n[!]Saliendo...')
    os._exit(1)


signal.signal(signal.SIGINT, signal_handler)

# Ejecución de comandos con vuelta de output y errores


def executionWithOutput(command):
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    return (result.stdout, result.stderr)

# Uso de ram

def ram(executable, Argumentos):
    if Argumentos:
        (out, err) = executionWithOutput(
            "./test/ram.sh -b " + executable + " -a \'" + Argumentos + "\'")
    else:
        (out, err) = executionWithOutput("./test/ram.sh -b " + executable)
    return out

# Uso de CPU


def cpuUse(executable, Argumentos):
    if Argumentos:
        (out, err) = executionWithOutput('./test/cpu.sh -b ' +
                                            executable + " -a \'" + Argumentos + "\'" + ' -t 1')
    else:
        (out, err) = executionWithOutput(
            './test/cpu.sh -b ' + executable + ' -t 1')
    return out

# Peso del binario


def peso(executable, Argumentos):
    (out, err) = executionWithOutput('./test/peso.sh ' + executable)
    return out

# Robustez del binario


def robustness(executable, Argumentos, Executions):
    if Argumentos:
        (out, err) = executionWithOutput(
            './test/robustez.sh -b ' + executable + ' -e ' + str(Executions) + ' -a \'' + Argumentos + '\'')
    else:
        (out, err) = executionWithOutput(
            './test/robustez.sh -b ' + executable + ' -e ' + str(Executions))
    return out

# Tiempo de ejecución


def exTime(executable, Argumentos):
    if Argumentos:
        (out, err) = executionWithOutput(
            './test/tiempo.sh \'' + executable + " " + Argumentos + "\'")
    else:
        (out, err) = executionWithOutput('./test/tiempo.sh ' + executable)
    numero = err.split(',')  # Time usa stderr para la salida
    out = float(numero[0] + '.' + numero[1])
    return out