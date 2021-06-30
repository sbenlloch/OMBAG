import os
import sys
import subprocess
import time
import copy


def selection(poblacion, N):
    poblacionAux = sorted(poblacion, key=lambda cromosoma: cromosoma.WSM)[:N]
    return poblacionAux


def converge(historico):
    copiaHistorico = copy.deepcopy(historico)
    anterior = sorted(copiaHistorico[-2], key=lambda cromosoma: cromosoma.WSM)[0]
    actual = sorted(copiaHistorico[-1], key=lambda cromosoma: cromosoma.WSM)[0]
    if anterior.tuplas == actual.tuplas:
        return True
    return False

def limites(Limite, Max_Gen, Gen, Max_Tiempo, Tiempo,Historico, Gen_Convergencia):
    if Limite == 0:
        if Max_Gen <= Gen:
            return True
    if Limite == 1:
        if Max_Tiempo <= (time.time() - Tiempo):
            return True
    if Limite == 2 and Gen > Gen_Convergencia:
        return converge(Historico)
    if Limite > 2:
        print("[!]Limite seleccionado fuera de rango")
        sys.exit(1)
    return False