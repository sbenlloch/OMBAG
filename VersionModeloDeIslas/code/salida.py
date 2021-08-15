import copy
import os


def imprimir(poblacion):
    for cromosoma in poblacion:
        print(
            "Resultados cromosoma "
            + str(cromosoma.id)
            + "\n\n"
            + "\tResultados pruebas: [ Ram: "
            + str(cromosoma.resultRam)
            + ",\n"
            + "\t                      Robustez: "
            + str(cromosoma.resultRob)
            + ",\n"
            + "\t                      Tiempo: "
            + str(cromosoma.resultTiempo)
            + ",\n"
            + "\t                      Peso: "
            + str(cromosoma.resultPeso)
            + ",\n"
            + "\t                      CPU: "
            + str(cromosoma.resultCPU)
            + " ]\n\n"
            + "\tResultados tras normalizar: [ Ram: "
            + str(cromosoma.afterNormRam)
            + ",\n"
            + "\t                              Robustez: "
            + str(cromosoma.afterNormRob)
            + ",\n"
            + "\t                              Tiempo: "
            + str(cromosoma.afterNormTiempo)
            + ",\n"
            + "\t                              Peso: "
            + str(cromosoma.afterNormPeso)
            + ",\n"
            + "\t                              CPU: "
            + str(cromosoma.afterNormCpu)
            + " ]\n\n"
            + "\tResultados WSM: "
            + str(cromosoma.WSM)
            + "\n\n\n"
        )


diccionarioIDs = {}
contadorIDs = -1


def sustituirID(id):
    global diccionarioIDs, contadorIDs
    if id not in diccionarioIDs:
        contadorIDs += 1
        diccionarioIDs[id] = contadorIDs
        return contadorIDs
    else:
        return diccionarioIDs[id]


def cantidadMejoresFlags(historico, directorioBase):
    diccionarioFlags = {}

    for generacion in historico:
        mejor = generacion[0]
        for cromosoma in generacion:
            if mejor.WSM > cromosoma.WSM:
                mejor = cromosoma
        for tupla in mejor.tuplas:
            if tupla[0] not in diccionarioFlags and tupla[1]:
                diccionarioFlags[tupla[0]] = 1
            elif tupla[0] in diccionarioFlags and tupla[1]:
                diccionarioFlags[tupla[0]] += 1

    archivoCantidad = directorioBase + "/CantidadFlagsMEJORES.csv"
    file = open(archivoCantidad, "w")
    file.write("Flag;Cantidad\n")
    for key in diccionarioFlags.keys():
        file.write(str(key) + ";" + str(diccionarioFlags[key]) + "\n")
    file.close()


def cantidadFlags(historico, directorioBase):
    diccionarioFlags = {}

    for generacion in historico:
        mejor = generacion[0]
        for cromosoma in generacion:
            for tupla in cromosoma.tuplas:
                if tupla[0] not in diccionarioFlags and tupla[1]:
                    diccionarioFlags[tupla[0]] = 1
                elif tupla[0] in diccionarioFlags and tupla[1]:
                    diccionarioFlags[tupla[0]] += 1

    archivoCantidad = directorioBase + "/CantidadFlagsTODOS.csv"
    file = open(archivoCantidad, "w")
    file.write("Flag;Cantidad\n")
    for key in diccionarioFlags.keys():
        file.write(str(key) + ";" + str(diccionarioFlags[key]) + "\n")
    file.close()


def archivosEstadisticas(historico, directorioBase, Ram, Tiempo, Peso, Rob, Cpu):

    if Ram:
        archivoRam = directorioBase + "/resultadosRam.csv"
        file = open(archivoRam, "w")
        file.write("ID;Generacion;Resultado\n")
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(
                    str(sustituirID(cromosoma.id))
                    + ";"
                    + str(i)
                    + ";"
                    + str(cromosoma.resultRam)
                    + "\n"
                )
        file.close()

    if Tiempo:
        archivoTiempo = directorioBase + "/resultadosTiempo.csv"
        file = open(archivoTiempo, "w")
        file.write("ID;Generacion;Resultado\n")
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(
                    str(sustituirID(cromosoma.id))
                    + ";"
                    + str(i)
                    + ";"
                    + str(cromosoma.resultTiempo)
                    + "\n"
                )
        file.close()

    if Peso:
        archivoPeso = directorioBase + "/resultadosPeso.csv"
        file = open(archivoPeso, "w")
        file.write("ID;Generacion;Resultado\n")
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(
                    str(sustituirID(cromosoma.id))
                    + ";"
                    + str(i)
                    + ";"
                    + str(cromosoma.resultPeso)
                    + "\n"
                )
        file.close()

    if Rob:
        archivoRob = directorioBase + "/resultadosRobustez.csv"
        file = open(archivoRob, "w")
        file.write("ID;Generacion;Resultado\n")
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(
                    str(sustituirID(cromosoma.id))
                    + ";"
                    + str(i)
                    + ";"
                    + str(cromosoma.resultRob)
                    + "\n"
                )
        file.close()

    if Cpu:
        archivoCpu = directorioBase + "/resultadosCPU.csv"
        file = open(archivoCpu, "w")
        file.write("ID;Generacion;Resultado\n")
        for i in range(len(historico)):
            for cromosoma in historico[i]:
                file.write(
                    str(sustituirID(cromosoma.id))
                    + ";"
                    + str(i)
                    + ";"
                    + str(cromosoma.resultCPU)
                    + "\n"
                )
        file.close()
    archivoWSM = directorioBase + "/resultadosWSM.csv"
    file = open(archivoWSM, "w")
    file.write("ID;Generacion;Resultado\n")
    for i in range(len(historico)):
        for cromosoma in historico[i]:
            file.write(
                str(sustituirID(cromosoma.id))
                + ";"
                + str(i)
                + ";"
                + str(cromosoma.WSM)
                + "\n"
            )
    file.close()

    cantidadMejoresFlags(historico, directorioBase)
    cantidadFlags(historico, directorioBase)
