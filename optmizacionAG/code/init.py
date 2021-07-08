import json
import time

import cromosoma
import flags


def inicializacionFlags(file):

    data = json.load(file)

    listaFlags = []
    for binarias in data['binarias']:
        nombre = str(binarias['flag'])
        objeto = flags.Flag(nombre)
        listaFlags.append(objeto)

    for rangos in data['rango']:
        nombre = str(rangos['flag'])
        minimo = int(rangos['min'])
        maximo = int(rangos['max'])
        objeto = flags.rangoFlag(nombre, minimo, maximo)
        listaFlags.append(objeto)

    for inter in data['Intervalo']:
        nombre = str(inter['flag'])
        intervalo = str(inter['intervalo']).split(',')
        objeto = flags.intervaloFLag(nombre, intervalo)
        listaFlags.append(objeto)

    return listaFlags


def tiempo():
    epoch = time.time()
    local = time.localtime(epoch)
    return '%d-%d-%d_%d:%d:%d' % (local.tm_mday, local.tm_mon, local.tm_year, local.tm_hour, local.tm_min, local.tm_sec)


def generarPoblacionAleatoria(tamaño, flags):
    population = []
    for _ in range(tamaño):
        population.append(cromosoma.generarCromosomaAleatorio(flags))
    return population
