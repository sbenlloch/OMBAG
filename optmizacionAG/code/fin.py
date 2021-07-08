import os
import subprocess
import time

from globales import *

import fitness


def executionWithOutput(command):
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    return (result.stdout, result.stderr)


def error(pathFile, salida, error, lineaComp):
    file = open(pathFile + 'errorCompilacion.txt', 'a')
    file.write('Error en compilacion.\nError GCC: \n' +
               str(error) + '\nSalida GCC:\n' + str(salida) + '\n')
    file.write('Linea de compilacion:\n' + str(lineaComp))
    file.close()


def compilarIndividuos(directorio, listaACompilar, programa, dependencias, flagsDependencias):
    directorioComparacion = directorio + '/comparacionFinal/'
    os.mkdir(directorioComparacion)
    cont = 0
    for opt in listaACompilar:
        directorioOpt = directorioComparacion + \
            'Optimizacion' + str(cont) + '/'
        os.mkdir(directorioOpt)
        nombreCompilacion = directorioOpt + 'optimizacion' + str(cont)
        lineaComp = 'gcc ' + programa + ' ' + dependencias + \
            ' -o ' + nombreCompilacion + ' ' + flagsDependencias + opt
        (out, err) = executionWithOutput(lineaComp)
        if err != '' or out != '':
            error(directorioOpt, out, err, lineaComp)
        cont += 1
    return directorioComparacion


def normAuxiliar(vector):
    min = float('inf')
    max = 0.0
    for elemento in vector:
        if elemento < min and elemento > 0.0:
            min = elemento
        if elemento > max and elemento > 0.0:
            max = elemento
    if min == max or min > max:
        for i in range(len(vector)):
            if vector[i] == min:
                vecgor[i] == 0.0
            else:
                vector[i] == 1.0
    else:
        for i in range(len(vector)):
            if vector[i] < 0.0:
                vector[i] = 1.0
            else:
                vector[i] = (vector[i] - min) / (max - min)


def test(directorioComparacion):
    resultRam = []
    resultCpu = []
    resultRob = []
    resultPeso = []
    resultTiempo = []
    globalResult = []
    for i in range(0, 8):
        directorioActual = directorioComparacion + \
            'Optimizacion' + str(i) + '/'
        optimizacionActual = directorioActual + 'optimizacion' + str(i)
        if Ram:
            resultRam.append(
                float(fitness.ram(optimizacionActual, Argumentos, directorioActual)))
        if Peso:
            resultPeso.append(
                float(fitness.peso(optimizacionActual, Argumentos, directorioActual)))
        if Cpu:
            resultCpu.append(float(fitness.cpuUse(
                optimizacionActual, Argumentos, directorioActual)))
        if Rob:
            robustezAux = fitness.robustness(
                optimizacionActual, Argumentos, ExecutionRobustness, directorioActual).split('\n')
            resultRob.append(1.0 - float(robustezAux[0]))
        if Tiempo:
            resultTiempo.append(float(fitness.exTime(
                optimizacionActual, Argumentos, directorioActual)))
    if len(resultRam) <= 0:
        resultRam = [0]*8
    else:
        normAuxiliar(resultRam)

    if len(resultCpu) <= 0:
        resultCpu = [0]*8

    if len(resultRob) <= 0:
        resultRob = [0]*8

    if len(resultTiempo) <= 0:
        resultTiempo = [0]*8
    else:
        normAuxiliar(resultTiempo)

    if len(resultPeso) <= 0:
        resultPeso = [0]*8
    else:
        normAuxiliar(resultPeso)

    for i in range(0, 8):
        globalResult.append(Ram*resultRam[i] + Peso*resultPeso[i] +
                            Cpu*resultCpu[i] + Rob*resultRob[i] + Tiempo*resultTiempo[i])

    lineasMaximas = 29
    for i in range(0, 8):
        globalResult[i] = int(globalResult[i] * 34 + 1)
    # Que pintar
    result = []
    result.append((' - Sin optimización <' + '-' *
                   globalResult[0] + '>', globalResult[0]))
    result.append((' - 00               <' + '-' *
                   globalResult[1] + '>', globalResult[1]))
    result.append((' - 01               <' + '-' *
                   globalResult[2] + '>', globalResult[2]))
    result.append((' - 02               <' + '-' *
                   globalResult[3] + '>', globalResult[3]))
    result.append((' - 03               <' + '-' *
                   globalResult[4] + '>', globalResult[4]))
    result.append((' - 0s               <' + '-' *
                   globalResult[5] + '>', globalResult[5]))
    result.append((' - 0fast            <' + '-' *
                   globalResult[6] + '>', globalResult[6]))
    result.append((' - 0ptimización AG  <' + '-' *
                   globalResult[7] + '>', globalResult[7]))
    result.sort(key=lambda tupla: tupla[1])
    print('\n [Comparación]: ')
    print(' [WSM]:')
    print(' De mejor a peor(less is better):\n')
    for element in result:
        print(element[0])


def comparacion(directorioBase, mejorCromosoma, programa, dependencias, flagsDependencias):
    estandar = ''
    opt0 = '-O0'
    opt1 = '-O1'
    opt2 = '-O2'
    opt3 = '-O3'
    size = '-Os'
    fast = '-Ofast'
    mejor = ''
    for tupla in mejorCromosoma.tuplas:
        if tupla[1]:
            mejor += ' ' + tupla[0]
    listaOpt = [estandar, opt0, opt1, opt2, opt3, size, fast, mejor]
    directorio = compilarIndividuos(
        directorioBase, listaOpt, programa, dependencias, flagsDependencias)
    test(directorio)


def salidaFin(historico, directorioBase, Gen, limite, tiempo_inicio, programa, dependencias, flagsDependencias):
    print(
        '\n\n\033[1;36m┌────────────────────────────────────────────────────────┐')
    print('│                  Ejecución finalizada                  │')
    print('└────────────────────────────────────────────────────────┘')
    if limite == 0:
        print(' Ejecución finalizada en ' + str(Gen) + ' generaciones.\n')
    elif limite == 1:
        print(' Ejecución finalizada en ' +
              str(round(time.time() - tiempo_inicio, 1)) + ' segundos.\n')
    elif limite == 2:
        print(' Ejecución finalizada por convergencia ejecución.\n')
    else:
        print('Límite fuera de rango')
    carpeta = directorioBase.split('/')[-1]
    print(' Se han generado automaticamente diferentes archivos de\n' +
          ' estadísticas de la ejecución, los puedes encontrar en la\n' +
          ' carpeta  ' + carpeta + ' en el path que has\n' +
          ' configurado.\n')
    print(' Antes de finalizar:\n')
    comparar = input(
        ' - ¿Quieres comparar el resultado con los flags de opti-\n   mización?[y/n]: ')
    if comparar == 'y':
        comparar = True
    else:
        comparar = False
    print('\n')
    print('--------------------------------------------------------\n\n')
    print(' Esta es la línea de compilación seleccionada: \n')
    ultimoSeleccionado = sorted(
        historico[-1], key=lambda cromosoma: cromosoma.WSM)[0]
    lineaCompilacion = ultimoSeleccionado.lineaCompilacion
    lineaCompToVect = lineaCompilacion.split(' ')
    path = '<path programa>'
    for palabra in lineaCompToVect:
        if '/' in palabra:
            palabra = path
        if '-o' in palabra:
            path = '<path ejecutable>'
        print(' ' + palabra, end='')
    print('\n')

    if comparar:
        comparacion(directorioBase, ultimoSeleccionado,
                    programa, dependencias, flagsDependencias)
