# Máximos y minimos globales
minGlobalRam = float("inf")
maxGlobalRam = 0.0
minGlobalTiempo = float("inf")
maxGlobalTiempo = 0.0
minGlobalPeso = float("inf")
maxGlobalPeso = 0.0


def normRam(poblacion):
    global minGlobalRam, maxGlobalRam
    # Buscar máximos y minimos
    for cromosoma in poblacion:
        if cromosoma.resultRam > 0.0 and cromosoma.resultRam > maxGlobalRam:
            maxGlobalRam = cromosoma.resultRam
        if cromosoma.resultRam > 0.0 and cromosoma.resultRam < minGlobalRam:
            minGlobalRam = cromosoma.resultRam
    # El segundo caso es extremo, no debería pasar nunca
    if minGlobalRam == maxGlobalRam or maxGlobalRam < minGlobalRam:
        for cromosoma in poblacion:
            if (
                cromosoma.resultRam == minGlobalRam
                or cromosoma.resultRam == maxGlobalRam
            ):
                cromosoma.afterNormRam = 0.0
            else:
                cromosoma.afterNormRam = 1.0
    else:
        for cromosoma in poblacion:
            if cromosoma.resultRam < 0.0:
                cromosoma.afterNormRam = 1.0
            else:
                cromosoma.afterNormRam = (cromosoma.resultRam - minGlobalRam) / (
                    maxGlobalRam - minGlobalRam
                )


def normTiempo(poblacion):
    global minGlobalTiempo, maxGlobalTiempo
    for cromosoma in poblacion:
        if cromosoma.resultTiempo > 0.0 and cromosoma.resultTiempo > maxGlobalTiempo:
            maxGlobalTiempo = cromosoma.resultTiempo
        if cromosoma.resultTiempo > 0.0 and cromosoma.resultTiempo < minGlobalTiempo:
            minGlobalTiempo = cromosoma.resultTiempo
    if minGlobalTiempo == maxGlobalTiempo or maxGlobalTiempo < minGlobalTiempo:
        for cromosoma in poblacion:
            if (
                cromosoma.resultTiempo == minGlobalTiempo
                or cromosoma.resultTiempo == maxGlobalTiempo
            ):
                cromosoma.afterNormTiempo = 0.0
            else:
                cromosoma.afterNormTiempo = 1.0
    else:
        for cromosoma in poblacion:
            if cromosoma.resultTiempo < 0.0:
                cromosoma.afterNormTiempo = 1.0
            else:
                cromosoma.afterNormTiempo = (
                    cromosoma.resultTiempo - minGlobalTiempo
                ) / (maxGlobalTiempo - minGlobalTiempo)


def normPeso(poblacion):
    global maxGlobalPeso, minGlobalPeso
    # Buscar máximos y minimos
    for cromosoma in poblacion:
        if cromosoma.resultPeso > 0.0 and cromosoma.resultPeso > maxGlobalPeso:
            maxGlobalPeso = cromosoma.resultPeso
        if cromosoma.resultPeso > 0.0 and cromosoma.resultPeso < minGlobalPeso:
            minGlobalPeso = cromosoma.resultPeso
    if minGlobalPeso == maxGlobalPeso or maxGlobalPeso < minGlobalPeso:
        for cromosoma in poblacion:
            if (
                cromosoma.resultPeso == minGlobalPeso
                or cromosoma.resultPeso == maxGlobalPeso
            ):
                cromosoma.afterNormPeso = 0.0
            else:
                cromosoma.afterNormPeso = 1.0
    else:
        for cromosoma in poblacion:
            if cromosoma.resultPeso < 0.0:
                cromosoma.afterNormPeso = 1.0
            else:
                cromosoma.afterNormPeso = (cromosoma.resultPeso - minGlobalPeso) / (
                    maxGlobalPeso - minGlobalPeso
                )


def normRob(poblacion):
    for cromosoma in poblacion:
        if cromosoma.resultRob < 0.0:
            cromosoma.afterNormRob = 1.0
        # Para elegir antes a uno que funciona que a uno que no
        # y que este entre 0 y 1 cambiamos los resultados iguales a 1.0 como 0.999
        elif cromosoma.resultRob == 1.0:
            cromosoma.afterNormRob = 0.999
        else:
            cromosoma.afterNormRob = cromosoma.resultRob


def normCpu(poblacion):
    for cromosoma in poblacion:
        if cromosoma.resultCPU < 0.0:
            cromosoma.afterNormCpu = 1.0
        # Para elegir antes a uno que funciona que a uno que no
        # y que este entre 0 y 1 cambiamos los resultados iguales a 1.0 como 0.999
        elif cromosoma.resultCPU == 1.0:
            cromosoma.afterNormCpu = 0.999
        else:
            cromosoma.afterNormCpu = cromosoma.resultCPU


def wsm(poblacion, Ram, Tiempo, Peso, Rob, CPU):
    for cromosoma in poblacion:
        cromosoma.WSM = (
            cromosoma.afterNormRam * Ram
            + cromosoma.afterNormTiempo * Tiempo
            + cromosoma.afterNormPeso * Peso
            + cromosoma.afterNormRob * Rob
            + cromosoma.afterNormCpu * CPU
        )
