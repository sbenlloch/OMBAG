import random
import time
import flags
import copy

class Cromosoma():

    resultRam  = 1.1 #Valor para aquellos que el test falle o no se tengan en cuenta para la optimización
    resultRob = 1.1
    resultTiempo = 1.1
    resultPeso = 1.1
    resultCPU = 1.1

    def __init__(self, flagsPropias, tuplas):
        self.flags = flagsPropias
        self.tuplas = tuplas
        self.id = int(time.time() * 10000)

    def setRam(self, ram):
        self.resultRam = ram
    def setRob(self, rob):
        self.resultRob = rob
    def setTiempo(self, tiempo):
        self.resultTiempo = tiempo
    def setPeso(self, peso):
        self.resultPeso = peso
    def setCPU(self, cpu):
        self.resultCPU = cpu


def generarCromosomaAleatorio(flags): #Devuelve un cromosoma aleatoriazando todas sus partes
    #mutar todas las flags para conseguir uno cromosoma completamente aleatorio
    for flag in flags:
        flag.mutateFlag()
    listaTuplas = []
    for flag in flags:
        listaTuplas.append(flag.getRandomTuple())
    NuevoCromosoma = Cromosoma(flags, listaTuplas)
    return NuevoCromosoma

def mutarCromosoma(cromosoma, radiacion):
    for i in range(radiacion):
        a_mutar = random.randint(0,len(cromosoma.flags)-1)
        flagSeleccionada = cromosoma.flags[a_mutar]
        cromosoma.flags[a_mutar].mutateFlag()
        cromosoma.tuplas[a_mutar] = flagSeleccionada.getRandomTuple()

def crossover(listaAntecedentes, cantidad_a_mutar, radiacion):
    tamaño = len(listaAntecedentes[0].flags)
    listaFlagsNuevo = []
    listaTuplasNuevo = []
    for i in range(tamaño):
        aleatorio = random.randint(0, len(listaAntecedentes) - 1)
        listaFlagsNuevo.append(listaAntecedentes[aleatorio].flags[i])
        listaTuplasNuevo.append(listaAntecedentes[aleatorio].tuplas[i])
    para_mutar = Cromosoma(listaFlagsNuevo, listaTuplasNuevo)
    for _ in range(cantidad_a_mutar): mutarCromosoma(para_mutar, radiacion)
    return para_mutar
