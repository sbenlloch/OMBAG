import matplotlib.pyplot as plt
import numpy as np
import sys


archivo = sys.argv[1]
lectura = open(archivo, "r")

texto = []

for line in lectura:
    texto.append(line)

tuplas = []
flag = []
cantidad = []

for line in texto[1:]:
    sinSalto = line.split("\n")[0]
    linea = sinSalto.split(";")
    tuplas.append((str(linea[0]), int(linea[1])))

sortedList = sorted(tuplas, key=lambda tup: tup[1])

for tupla in sortedList:
    flag.append(tupla[0])
    cantidad.append(tupla[1])

x = np.array(flag)
y = np.array(cantidad)
width = 0.4
plt.figure(figsize=(6, 13))
fig = plt.barh(x, y, width, align="center", color="mediumslateblue")
plt.subplots_adjust(
    left=0.5, right=0.9, top=0.975, bottom=0.05, wspace=0.05, hspace=0.05
)
# plt.xticks(cantidad, flag, rotation=30)
plt.ylabel("Cantidad")
plt.xlabel("Flags")
plt.title("Distribución Flags")
lista = []
for i, v in enumerate(y):
    if int(v) not in lista:
        plt.text(v, i, str(v), color="dimgray", fontweight="bold")
        lista.append(v)
plt.show()
