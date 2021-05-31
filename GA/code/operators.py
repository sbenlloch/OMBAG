import signal
import os

def signal_handler(sig, frame):
    print('\n[!]Saliendo...')
    os._exit(1)


signal.signal(signal.SIGINT, signal_handler)

# Normalizar pesos, dato un vector y su tamaño se normalizan entre 0 y 1, devuelve el vector normalizado

def normalizar(vector, N):
    # buscando maximos y minimos
    max = 0.0
    min = float('inf')
    for j in range(0, N):

        if min > vector[j] and not(vector[j] < 0):
            min = vector[j]
        if max < vector[j] and not(vector[j] < 0):
            max = vector[j]

    if (max - min) == 0.0:
        return vector

    for j in range(0, N):
        if vector[j] < 0:
            vector[j] = 1.1  # revisar
        else:
            vector[j] = (vector[j] - min) / (max - min)

    return vector

# WSM, dado los resultados de las diferentes pruebas aplica los pesos y devuelve un vector con el resultado


def WSM(matrix, N, Ram, Cpu, Peso, Rob, Tiempo):
    result = []
    for i in range(0, N):
        wsm = matrix[0][i]*Ram + matrix[1][i]*Cpu + matrix[2][i] * \
            Peso + matrix[3][i]*Rob + matrix[4][i]*Tiempo
        result.append(wsm)
    return result