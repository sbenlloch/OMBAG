
def normRam(poblacion):
    max = 0.0
    min = float('inf')
    # Buscar máximos y minimos
    for cromosoma in poblacion:
        if cromosoma.resultRam > 0.0 and cromosoma.resultRam > max:
            max = cromosoma.resultRam
        if cromosoma.resultRam > 0.0 and cromosoma.resultRam < min:
            min = cromosoma.resultRam
    if min == max or max < min:
        for cromosoma in poblacion:
            if cromosoma.resultRam == min or cromosoma.resultRam == max:
                cromosoma.afterNormRam = 0.0
            else:
                cromosoma.afterNormRam = 1.0
    else:
        for cromosoma in poblacion:
            if cromosoma.resultRam < 0.0:
                cromosoma.afterNormRam = 1.0
            else:
                cromosoma.afterNormRam = (
                    cromosoma.resultRam - min) / (max - min)


def normTiempo(poblacion):
    max = 0.0
    min = float('inf')
    for cromosoma in poblacion:
        if cromosoma.resultTiempo > 0.0 and cromosoma.resultTiempo > max:
            max = cromosoma.resultTiempo
        if cromosoma.resultTiempo > 0.0 and cromosoma.resultTiempo < min:
            min = cromosoma.resultTiempo
    if min == max or max < min:
        for cromosoma in poblacion:
            if cromosoma.resultTiempo == min or cromosoma.resultTiempo == max:
                cromosoma.afterNormTiempo = 0.0
            else:
                cromosoma.afterNormTiempo = 1.0
    else:
        for cromosoma in poblacion:
            if cromosoma.resultTiempo < 0.0:
                cromosoma.afterNormTiempo = 1.0
            else:
                cromosoma.afterNormTiempo = (
                    cromosoma.resultTiempo - min) / (max - min)


def normPeso(poblacion):
    max = 0.0
    min = float('inf')
    # Buscar máximos y minimos
    for cromosoma in poblacion:
        if cromosoma.resultPeso > 0.0 and cromosoma.resultPeso > max:
            max = cromosoma.resultPeso
        if cromosoma.resultPeso > 0.0 and cromosoma.resultPeso < min:
            min = cromosoma.resultPeso
    if min == max or max < min:
        for cromosoma in poblacion:
            if cromosoma.resultPeso == min or cromosoma.resultPeso == max:
                cromosoma.afterNormPeso = 0.0
            else:
                cromosoma.afterNormPeso = 1.0
    else:
        for cromosoma in poblacion:
            if cromosoma.resultPeso < 0.0:
                cromosoma.afterNormPeso = 1.0
            else:
                cromosoma.afterNormPeso = (
                    cromosoma.resultPeso - min) / (max - min)


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
        cromosoma.WSM = cromosoma.afterNormRam * Ram + cromosoma.afterNormTiempo * Tiempo + \
            cromosoma.afterNormPeso * Peso + cromosoma.afterNormRob * Rob + cromosoma.afterNormCpu * CPU
