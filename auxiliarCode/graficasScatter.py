import matplotlib.pyplot as plt
import numpy as np
import sys

archivo = sys.argv[1]
lectura = open(archivo, "r")

texto = []

for line in lectura:
    texto.append(line)

Id = []
Generacion = []
Valor = []

for line in texto[1:]:
    sinSalto = line.split("\n")[0]
    linea = sinSalto.split(";")

    if float(linea[2]) >= 0:
        Id.append(int(linea[0]))
        Generacion.append(int(linea[1]))
        Valor.append(float(linea[2]))


x = np.array(Generacion)
y = np.array(Valor)

plt.xlabel("Generación")
plt.ylabel("Valor")
try:
    plt.title(sys.argv[2])
except:
    pass
plt.scatter(x, y, c=x, cmap="turbo")
plt.show()

GeneracionActual = 0
MinimoActual = float("inf")
PosicionMinimoActual = 0

ValoresMinimos = []
GeneracionesMinimas = []
IdMinimos = []

for i, generacion in enumerate(Generacion):
    if GeneracionActual == generacion:
        if MinimoActual > Valor[i]:
            MinimoActual = Valor[i]
            PosicionMinimoActual = i
    else:
        ValoresMinimos.append(Valor[PosicionMinimoActual])
        GeneracionesMinimas.append(Generacion[PosicionMinimoActual])
        IdMinimos.append(Id[PosicionMinimoActual])
        MinimoActual = Valor[i]
        PosicionMinimoActual = i
        GeneracionActual = generacion


x = np.array(GeneracionesMinimas)
y = np.array(ValoresMinimos)

plt.xlabel("Generación")
plt.ylabel("Valores Minimos")
try:
    plt.title(sys.argv[3])
except:
    pass
plt.scatter(x, y, c=IdMinimos, cmap="nipy_spectral")
plt.show()

Acumulador = 0.0
GeneracionAcumulador = []
Medias = []
Contador = 1.0
GeneracionActual = 0

for i, generacion in enumerate(Generacion):
    if GeneracionActual != generacion:
        GeneracionAcumulador.append(GeneracionActual)
        Medias.append(Acumulador / Contador)
        Contador = 1.0
        Acumulador = Valor[i]
        GeneracionActual = generacion
    else:
        Acumulador += Valor[i]
        Contador += 1.0

x = np.array(GeneracionAcumulador)
y = np.array(Medias)

plt.xlabel("Generación")
plt.ylabel("Suma valores")
try:
    plt.title(sys.argv[4])
except:
    pass
plt.scatter(x, y, c=x, cmap="turbo")

plt.show()
