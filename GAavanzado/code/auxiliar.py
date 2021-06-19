import os
import subprocess
import time


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
    file.write('Error en compilacion.\nError GCC: \n' +
                str(error) + '\nSalida GCC:\n' + str(salida) + '\n')
    file.write('Linea de compilacion:\n' + str(lineaComp))
    file.close()


def compilarIndividuos(directorio, Gen, poblacion, programa):
    directorioGeneracion = directorio + '/Gen' + str(Gen) + '/'
    os.system('mkdir ' + directorioGeneracion)
    Cromosoma = 0
    for individuo in poblacion:
        directorioCromosoma = directorioGeneracion + \
            'Cromosoma' + str(Cromosoma) + '/'
        os.system('mkdir ' + directorioCromosoma)
        tuplas = individuo.tuplas
        flagsComp = stringFlags(tuplas)
        directorioCompActual = directorioCromosoma + \
            'Cromosoma' + str(Cromosoma)
        lineaComp = 'gcc ' + programa + ' -o ' + directorioCompActual + flagsComp
        (out, err) = executionWithOutput(lineaComp)
        if out != '' or err != '':
            error(directorioCromosoma, out, err, lineaComp)
        Cromosoma += 1
    return directorioGeneracion


def imprimir(poblacion):
    for cromosoma in poblacion:
        print("Resultados cromosoma " + str(cromosoma.id) + "\n\n" +
                "\tResultados pruebas: [ Ram: " + str(cromosoma.resultRam) + ',\n' +
                "\t                      Robustez: " + str(cromosoma.resultRob) + ',\n' +
                "\t                      Tiempo: " + str(cromosoma.resultTiempo) + ',\n' +
                "\t                      Peso: " + str(cromosoma.resultPeso) + ',\n' +
                "\t                      CPU: " + str(cromosoma.resultCPU) + ' ]\n\n' +
                "\tResultados tras normalizar: [ Ram: " + str(cromosoma.afterNormRam) + ',\n' +
                "\t                              Robustez: " + str(cromosoma.afterNormRob) + ',\n' +
                "\t                              Tiempo: " + str(cromosoma.afterNormTiempo) + ',\n' +
                "\t                              Peso: " + str(cromosoma.afterNormPeso) + ',\n' +
                "\t                              CPU: " + str(cromosoma.afterNormCpu) + ' ]\n\n' +
                "\tResultados WSM: " + str(cromosoma.WSM) + '\n\n\n')

def selection(poblacion, N):
    poblacionAux = sorted(poblacion, key=lambda cromosoma : cromosoma.WSM)[:N]
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
        if Max_Gen == Gen:
            return True
    if Limite == 1:
        if Max_Tiempo <= (time.time() - Tiempo):
            return True
    if Limite == 2:
        return converge(Convergencia, Historico)
    return False

def para_finalizar(historico, directorioBase):
    pass