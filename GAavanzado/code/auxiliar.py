import os
import subprocess

def stringFlags(tuplas):
    dev = ' '
    for tupla in tuplas:
        if tupla[1] == 1:
            dev += tupla[0] + ' '
    return dev

def executionWithOutput(command):
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    return (result.stdout, result.stderr)

def error(pathCromosoma, salida, error, lineaComp):
    file = open(pathCromosoma + 'errorCompilacion.txt', 'a')
    file.write('Error en compilacion.\nError GCC: \n'+ str(error) + '\nSalida GCC:\n' + str(salida) + '\n')
    file.write('Linea de compilacion:\n' + str(lineaComp))
    file.close()

def compilarIndividuos(directorio, Gen, poblacion, programa):
    directorioGeneracion = directorio + '/Gen' + str(Gen) + '/'
    os.system('mkdir ' + directorioGeneracion)
    Cromosoma = 0
    for individuo in poblacion:
        directorioCromosoma = directorioGeneracion + 'Cromosoma' + str(Cromosoma) + '/'
        os.system('mkdir ' + directorioCromosoma)
        tuplas = individuo.tuplas
        flagsComp = stringFlags(tuplas)
        directorioCompActual = directorioCromosoma + 'Cromosoma' + str(Cromosoma)
        lineaComp = 'gcc ' + programa + ' -o ' + directorioCompActual + flagsComp
        (out, err) = executionWithOutput(lineaComp)
        if out != '' or err != '':
            error(directorioCromosoma, out, err, lineaComp)
        Cromosoma += 1
    return directorioGeneracion