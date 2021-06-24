import os
import subprocess
import time
import copy


def selection(poblacion, N):
    poblacionAux = sorted(poblacion, key=lambda cromosoma: cromosoma.WSM)[:N]
    return poblacionAux


def media(generacion):
    acumulador = 0.0
    for cromosoma in generacion:
        acumulador += cromosoma.WSM
    return acumulador/len(generacion)


def converge(Converge, historico):
    if len(historico) < 2:
        return False
    else:
        actual = historico[-1:][0]
        anterior = historico[-2:-1][0]
        convergencia = 1.0 - (media(actual) / media(anterior))
        if convergencia > -0.01 and convergencia < Converge:
            return True
    return False


def end(Limite, Max_Gen, Gen, Max_Tiempo, Tiempo, Convergencia, Historico):
    if Limite == 0:
        if Max_Gen <= Gen:
            return True
    if Limite == 1:
        if Max_Tiempo <= (time.time() - Tiempo):
            return True
    if Limite == 2:
        return converge(Convergencia, Historico)
    return False