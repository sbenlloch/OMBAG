import time
import os
import subprocess

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

def compilarIndividuos(directorio,listaACompilar, programa, dependencias, flagsDependencias):
    directorioComparacion = directorio + '/comparacionFinal/'
    os.mkdir(directorioComparacion)
    cont = 0
    for opt in listaACompilar:
        directorioOpt = directorioComparacion + 'Optimizacion' + str(cont) + '/'
        os.mkdir(directorioOpt)
        nombreCompilacion = directorioOpt + 'optimizacion' + str(cont)
        lineaComp = 'gcc ' + programa + ' ' + dependencias + ' -o ' + nombreCompilacion + ' ' + flagsDependencias + opt
        (out, err) = executionWithOutput(lineaComp)
        if err!='' or out!='':
            error(directorioOpt, out, err, lineaComp)
        cont += 1
    return directorioComparacion

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
    directorio = compilarIndividuos(directorioBase, listaOpt, programa, dependencias, flagsDependencias)

def salidaFin(historico, directorioBase, Gen, limite, tiempo_inicio, programa, dependencias, flagsDependencias):
    print('\n\n\033[1;36m┌────────────────────────────────────────────────────────┐')
    print('│                  Ejecución finalizada                  │')
    print('└────────────────────────────────────────────────────────┘')
    if limite == 0:
        print(' Ejecución finalizada en ' + str(Gen) +' generaciones.\n')
    elif limite == 1:
        print(' Ejecución finalizada en ' + str(round(time.time() - tiempo_inicio, 1)) + ' segundos.\n')
    elif limite == 2:
        print(' Ejecución finalizada por convergencia ejecución.\n')
    else:
        print('Límite fuera de rango')
    carpeta = directorioBase.split('/')[-1]
    print(' Se han generado automaticamente diferentes archivos de\n' +
        ' estadísticas de la ejecución, los puedes encontrar en la\n' +
        ' carpeta  ' + carpeta +' en el path que has\n' +
        ' configurado.\n')
    print(' Antes de finalizar:\n')
    comparar = input(' - ¿Quieres comparar el resultado con los flags de opti-\n   mización?[y/n]: ')
    if comparar == 'y':
        comparar=True
    else:
        comparar=False
    print('\n')
    print('--------------------------------------------------------\n\n')
    print(' Esta es la línea de compilación seleccionada: \n')
    ultimoSeleccionado = sorted(historico[-1], key=lambda cromosoma: cromosoma.WSM)[0]
    lineaCompilacion = ultimoSeleccionado.lineaCompilacion
    lineaCompToVect = lineaCompilacion.split(' ')
    cont=0
    path = '<path programa>'
    for palabra in lineaCompToVect:
        if '/' in palabra:
            palabra = path
        if '-o' in palabra:
            path='<path ejecutable>'
        if cont == 2:
            print(' ' + palabra)
            cont = 0
        else:
            print(' ' + palabra, end='')
            cont+=1
    print('\n')
    if comparar:
        comparacion(directorioBase, ultimoSeleccionado, programa, dependencias, flagsDependencias)