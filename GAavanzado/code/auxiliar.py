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
        if Max_Gen <= Gen:
            return True
    if Limite == 1:
        if Max_Tiempo <= (time.time() - Tiempo):
            return True
    if Limite == 2:
        return converge(Convergencia, Historico)
    return False

diccionarioIDs = {}
contadorIDs = -1
def sustituirID(id):
    global diccionarioIDs, contadorIDs
    if (id not in diccionarioIDs):
        contadorIDs+=1
        diccionarioIDs[id] = contadorIDs
        return contadorIDs
    else: return diccionarioIDs[id]


def cantidadFlags(historico, directorioBase):
    diccionarioFlags={}
    for generacion in historico:
        for cromosoma in generacion:
            for tupla in cromosoma.tuplas:
                if tupla[0] not in diccionarioFlags and tupla[1]:
                    diccionarioFlags[tupla[0]] = 1
                elif tupla[0] in diccionarioFlags and tupla[1]:
                    diccionarioFlags[tupla[0]]+=1
    archivoCantidad = directorioBase + '/cantidadFlags.csv'
    file = open(archivoCantidad, 'w')
    file.write('Flag;Cantidad\n')
    for key in diccionarioFlags.keys():
        file.write(str(key)+';'+str(diccionarioFlags[key])+'\n')
    file.close()


def distribucionFlags(historico, directorioBase):
    diccionarioFlags={}
    for i in range(len(historico)):
        for cromosoma in historico[i]:
            for tupla in cromosoma.tuplas:
                if tupla[0] not in diccionarioFlags and tupla[1]:
                    diccionarioFlags[tupla[0]] = [i]
                elif tupla[0] in diccionarioFlags and tupla[1] and i not in diccionarioFlags[tupla[0]]:
                    diccionarioFlags[tupla[0]].append(i)
    archivoDistribucion = directorioBase + '/distribucionFlags.csv'
    file = open(archivoDistribucion, 'w')
    file.write('Flag;Generaciones\n')
    for key in diccionarioFlags.keys():
        file.write(str(key))
        for gen in diccionarioFlags[key]:
            file.write(';'+str(gen))
        file.write('\n')
    file.close()



def para_finalizar(historico, directorioBase, Ram, Tiempo, Peso, Rob, Cpu):
    if Ram:
        archivoRam = directorioBase + '/resultadosRam.csv'
        file = open(archivoRam, 'w')
        file.write('ID;Generacion;Resultado\n')
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(str(sustituirID(cromosoma.id))+';'+str(i)+';'+str(cromosoma.resultRam)+'\n')
        file.close()

    if Tiempo:
        archivoTiempo = directorioBase + '/resultadosTiempo.csv'
        file = open(archivoTiempo, 'w')
        file.write('ID;Generacion;Resultado\n')
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(str(sustituirID(cromosoma.id))+';'+str(i)+';'+str(cromosoma.resultTiempo)+'\n')
        file.close()

    if Peso:
        archivoPeso = directorioBase + '/resultadosPeso.csv'
        file = open(archivoPeso, 'w')
        file.write('ID;Generacion;Resultado\n')
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(str(sustituirID(cromosoma.id))+';'+str(i)+';'+str(cromosoma.resultPeso)+'\n')
        file.close()

    if Rob:
        archivoRob = directorioBase + '/resultadosRobustez.csv'
        file = open(archivoRob, 'w')
        file.write('ID;Generacion;Resultado\n')
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(str(sustituirID(cromosoma.id))+';'+str(i)+';'+str(cromosoma.resultRob)+'\n')
        file.close()

    if Cpu:
        archivoCpu = directorioBase + '/resultadosCPU.csv'
        file = open(archivoCpu, 'w')
        file.write('ID;Generacion;Resultado\n')
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(str(sustituirID(cromosoma.id))+';'+str(i)+';'+str(cromosoma.resultCPU)+'\n')
        file.close()

    archivoWSM = directorioBase + '/resultadosWSM.csv'
    file = open(archivoWSM, 'w')
    file.write('ID;Generacion;Resultado\n')
    for i in range(len(historico)):
        for cromosoma in historico[i]:
            file.write(str(sustituirID(cromosoma.id))+';'+str(i)+';'+str(cromosoma.WSM)+'\n')
    file.close()
    cantidadFlags(historico, directorioBase)
    distribucionFlags(historico, directorioBase)