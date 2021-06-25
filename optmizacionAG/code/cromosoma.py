import random
import time
import flags
import copy


class Cromosoma():

    resultRam = -1.0  # Valor para aquellos que el test falle o no se tengan en cuenta para la optimización
    resultRob = -1.0
    resultTiempo = -1.0
    resultPeso = -1.0
    resultCPU = -1.0

    # La normalización se encuentra entre 0 y 1 por lo tanto se va a seleccionar
    afterNormRam = 1.0   # 1 como peor caso para los que no funcionen
    afterNormTiempo = 1.0
    afterNormPeso = 1.0
    afterNormCpu = 1.0
    afterNormRob = 1.0

    # Resultado tras ponderar pesos
    WSM = 1.0

    #Línea de compilación del cromosoma
    lineaCompilacion = ''

    def __init__(self, flagsPropias, tuplas):
        self.flags = flagsPropias
        self.tuplas = tuplas
        self.id = int(time.time() * 10000000)


# Devuelve un cromosoma aleatoriazando todas sus partes
def generarCromosomaAleatorio(flags):
    # mutar todas las flags para conseguir uno cromosoma completamente aleatorio
    for flag in flags:
        flag.mutateFlag()
    listaTuplas = []
    # Generar tupla aleatoria para cada flag
    for flag in flags:
        listaTuplas.append(flag.getRandomTuple())
    # Crear cromosoma y devolver
    NuevoCromosoma = Cromosoma(flags, listaTuplas)
    return NuevoCromosoma


# Muta un cromosoma aleatoriamente la cantidad de veces que se indique en el parámetro radiación
def mutarCromosoma(cromosoma, radiacion):
    for i in range(radiacion):
        # Posicion aleatoria a mutars
        a_mutar = random.randint(0, len(cromosoma.flags)-1)
        flagSeleccionada = cromosoma.flags[a_mutar]
        cromosoma.flags[a_mutar].mutateFlag()  # mutar flag
        # actualizar flag y aleatoriazar
        cromosoma.tuplas[a_mutar] = flagSeleccionada.getRandomTuple()


# Cruza cromosomas aleatoriamente, muta el cromosoma resultante tantas veces como se indique en cantidad_a_mutar
def crossover(listaAntecedentes, radiacion):
    tamaño = len(listaAntecedentes[0].flags)  # Cantidad de flags
    listaFlagsNuevo = []
    listaTuplasNuevo = []
    for i in range(tamaño):
        # Selección aleatoria del cromosoma padre
        aleatorio = random.randint(0, len(listaAntecedentes) - 1)
        listaFlagsNuevo.append(listaAntecedentes[aleatorio].flags[i])
        listaTuplasNuevo.append(listaAntecedentes[aleatorio].tuplas[i])
    # Crear cromosoma
    para_mutar = Cromosoma(listaFlagsNuevo, listaTuplasNuevo)
    mutarCromosoma(para_mutar, radiacion)  # Mutar cromosoma
    return para_mutar

'''
Devuelve la siguiente generación, creada a partir de la anterior
y del porcentaje de poblacion aleatorio en cada nueva generación.
    entrada:
        selected --> individuos de la población anterior seleccionados
        tamaño --> tamaño de la siguiente población
        aleatorios --> porcentaje de aleatorios de la nueva población
        radiacion --> cantidad de veces máxima que se muta a en los crossover
        Devuelve una lista de Cromosomas
'''
def siguienteGeneracion(selected, tamaño, aleatorios, radiacion, flags):
    nuevaPoblacion = []
    cantidad_aleatorios = int(tamaño*aleatorios)
    cantidad_cruzados = tamaño - len(selected) - cantidad_aleatorios
    nuevaPoblacion += selected
    for _ in range(cantidad_aleatorios):
        nuevaPoblacion.append(generarCromosomaAleatorio(flags))
    for _ in range(cantidad_cruzados):
        nuevaPoblacion.append(crossover(selected, radiacion))
    return nuevaPoblacion