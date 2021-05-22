import random
import os
import sys
import time
import configparser
import subprocess
"""
    Declaracion de variables globales
"""

flags = []
population = []
parser = configparser.ConfigParser()
parser.read('conf.ini')
# Peso objetivos
Ram = float(parser['Settings']['Ram'])
Cpu = float(parser['Settings']['CPU'])
Peso = float(parser['Settings']['Peso'])
Rob = float(parser['Settings']['Robustez'])
Tiempo = float(parser['Settings']['Tiempo'])
#tamaño población
Num_Pob = int(parser['Settings']['N_Poblacion'])
#path a archivo con flags elegidas
Path = parser['Flags']['Path']
#Tiempo inicial
timestamp = ''
#directorio global
pathGlobal = ''
#archivo log global
logGlobal = ''
#Path generacion actual
pathGen = ''
#Path log generacion actual
logLocalGen = ''
#Número de Generación
Gen = 0
#Limites
Max_Gen = int(parser['Limites']['Max_Gen'])
#Binario a optimizar
Binario = sys.argv[1]

def createPop(N):
    for i in range(0, N):
        cromo = []
        for flag in flags:
            tupla = (random.randint(0,1) , flag)
            cromo.append(tupla)
        population.append(cromo)

def tiempo():
    epoch = time.time()
    local = time.localtime(epoch)
    return '%d.%d.%d.%d.%d.%d' % (local.tm_mday, local.tm_mon, local.tm_year, local.tm_hour, local.tm_min, local.tm_sec)
def inicializacionLog():
    global timestamp
    global pathGlobal
    global logGlobal
    epoch = time.time()
    local = time.localtime(epoch)
    timestamp = '%d.%d.%d.%d.%d.%d' % (local.tm_mday, local.tm_mon, local.tm_year, local.tm_hour, local.tm_min, local.tm_sec)
    print('Ejecución iniciada en ' + timestamp)
    os.system('mkdir /tmp/algorithmExecution'+timestamp)
    pathGlobal = '/tmp/algorithmExecution'+timestamp
    pathGlobalFile = '/tmp/algorithmExecution'+timestamp+'/logGlobal.txt'
    os.system('touch ' + pathGlobalFile)
    logGlobal = open(pathGlobalFile, 'a')
    logGlobal.write('Execution started in ' + timestamp + '\n')
    logGlobal.write('Population Size: ' + str(Num_Pob) + '\n')
    logGlobal.write('Weight: ' + '\n')
    logGlobal.write('\tRam: ' + str(Ram) + '\n')
    logGlobal.write('\tTime: ' + str(Tiempo) + '\n')
    logGlobal.write('\tCpu load: ' + str(Cpu) + '\n')
    logGlobal.write('\tRobustness: ' + str(Rob) + '\n')
    logGlobal.write('\tBinary Weigth: ' + str(Peso) + '\n')
    logGlobal.write('\nFlags:\n')
    logGlobal.write('\t' + str(flags) + '\n')

def inicializaGen(N, pob):
    global pathGen
    global logLocalGen
    pathGen =  pathGlobal + '/Gen' + str(N)
    os.system('mkdir ' + pathGen)
    pathLocalFile = pathGen + '/localFileGen' + str(N)
    os.system('touch ' + pathLocalFile)
    logLocalGen = open(pathLocalFile , 'a')
    epoch = time.time()
    local = time.localtime(epoch)
    timestamp = '%d.%d.%d.%d.%d.%d' % (local.tm_mday, local.tm_mon, local.tm_year, local.tm_hour, local.tm_min, local.tm_sec)
    logLocalGen.write('Generation start: ' + timestamp + '\n')
    for ind in range(0, pob):
        pathChromo = pathGen + '/Chromo' + str(ind)
        os.system('mkdir ' + pathChromo)
        os.system('touch ' + pathChromo + '/log' + 'Gen' + str(N) + '_Ind' + str(ind))

def test(chromosoma, N):
    pathChromo = pathGen + '/Chromo' + str(N)
    logChromo = pathGen + '/Chromo' + str(N) + '/logGen' + str(Gen) + '_Ind' + str(N)
    log = open(logChromo, 'a')
    log.write('Executed at ' + tiempo() + '\n')
    log.write('Chromosoma: \n')
    log.write('\t' + str(chromosoma) + '\n')
    line = ''
    for flag in chromosoma:
        if flag[0]:
            line += flag[1] + ' '
    line = 'gcc ' + Binario + ' -o ' + pathChromo + '/Chromo' + str(N) + ' ' + line
    log.write('Compilation line: \n')
    log.write('\t' + line + '\n')
    log.write('Output after compile: \n\t')
    os.popen(line) # falta salida de errores a archivo de logs


def main():
    global Gen, Max_Gen
    file = open(Path , 'r' ).read().split('\n')
    for line in file:
        if line:
            flags.append(line)
    inicializacionLog()
    createPop(Num_Pob)
    #para bucle de generaciones
    for i in range(0,Max_Gen):
        inicializaGen(Gen, Num_Pob)
        for i in range(0, len(population)):
            test(population[i], i)
        Gen+=1
    #...



if __name__ == "__main__":
    main()

logGlobal.close()
logLocalGen.close()

"""
    todas = ''
    for flag in flags:
        todas += flag + ' '
    print(todas)
"""