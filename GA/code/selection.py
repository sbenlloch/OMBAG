import random
import signal
import os

def signal_handler(sig, frame):
    print('\n[!]Saliendo...')
    os._exit(1)


signal.signal(signal.SIGINT, signal_handler)

flags = []

# Selection function, se seleccionan los mejores, indicando cuantos en el campo 'to_select', devuelve su posicion en la población y los valores elejidos

def selection(vector, to_select):
    sorted_vector = sorted(vector)
    selected_index = []
    for N in range(to_select):
        index = vector.index(sorted_vector[N])
        selected_index.append(index)
        vector[index] = None
    return (sorted(selected_index), sorted_vector[:to_select])

# Genera un número indicado en 'aleatorios' y devuelve añadiendo en 'populationIni' individuos aleatorios


def gen_aleatorios(populationIni, aleatorios):
    for i in range(0, aleatorios):
        cromo = []
        for flag in flags:
            tupla = (random.randint(0, 1), flag)
            cromo.append(tupla)
        populationIni.append(cromo)
    return populationIni

# Muta(Cambia) de forma aleatoria tantos bits como se indique en Radiación


def mutar(individuo, n_flags, Radiacion):
    for i in range(Radiacion % len(individuo)):
        individuo[random.randint(
            0, n_flags-1)] = abs(individuo[random.randint(0, n_flags-1)] - 1)
    return individuo

# Genera un individuo a partir de los que se pasen en 'antecesores'


def mezclar(antecesores, Radiacion):
    individuo = []
    n_antecesores = len(antecesores)
    n_flags = len(flags)
    for i in range(n_flags):
        gen = antecesores[i % n_antecesores][i]
        individuo.append(gen)
    individuo = mutar(individuo, n_flags, Radiacion)
    individuo_final = []
    for j in range(n_flags):
        individuo_final.append((individuo[j], flags[j]))
    return individuo_final

# Añade a 'poblacionIni' el número que se indique en 'N_mutar' de individuos a partir de 'antecesores'


def gen_mutados(poblacionIni, antecesores, N_mutar, Radiacion):
    for i in range(N_mutar):
        mezclado = mezclar(antecesores, Radiacion)
        poblacionIni.append(mezclado)
    return poblacionIni

# Genera población descendiente a partir de los antecesores indicados en 'slectionIndex'


def generarDescendientes(selectionIndex, population, Num_Pob, N_Select, Por_Random, list_flags, Radiacion):
    global flags
    flags = list_flags
    selected = []
    binaryFlags = []
    auxiliar = []
    populationAux = []

    for i in selectionIndex:
        selected.append(population[i])
        populationAux.append(population[i])
        for binary in population[i]:
            auxiliar.append(binary[0])
        binaryFlags.append(auxiliar)
        auxiliar = []
    aleatorios = int((Num_Pob - N_Select) * Por_Random)
    mutados = Num_Pob - aleatorios - N_Select
    populationAux = gen_aleatorios(populationAux, aleatorios)
    populationAux = gen_mutados(populationAux, binaryFlags, mutados, Radiacion)

    return populationAux