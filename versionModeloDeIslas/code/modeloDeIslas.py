import random


def intercambiar(poblaciones, N):
    pesos = [100] * len(poblaciones)
    for poblacion in poblaciones:
        selected = getMejores(N, poblacion)
        posicionElegido = random.choices(range(len(poblaciones)), weights=pesos)[0]
        pesos[posicionElegido] = 0
        cambio(poblaciones[posicionElegido], selected)


def getMejores(N, poblacion):
    poblacionAux = sorted(poblacion, key=lambda cromosoma: cromosoma.WSM)[:N]
    return poblacionAux


def cambio(poblacion, seleccionados):
    sorted(poblacion, key=lambda cromosoma: cromosoma.WSM)
    for posicion in range(len(poblacion) - 1, 0, -1):
        for seleccionado in seleccionados:
            poblacion[posicion] = seleccionado
