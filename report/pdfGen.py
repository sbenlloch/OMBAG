from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import matplotlib.pyplot as plot
import sys


est = sys.argv[1]
archivo = open(est, 'r')
line = []
Gen = []
Ram = []
Peso = []
Tiempo = []
Robustez = []
Cpu = []
w, h = A4
nombre_archivo = est.split('/')
nombre_archivo = nombre_archivo.pop()
nombre_archivo = nombre_archivo.split('.')
nombre_archivo = nombre_archivo[0] + '.pdf'
pdf = canvas.Canvas(nombre_archivo, pagesize=A4)
pdf.setTitle("Reporte resultados Optimización")
x = 50
y = h - 50
pdf.line(x, y, x + 200, y)
pdf.showPage()
pdf.save()

for linea in archivo:
    line = linea.split ('\t')
    Gen.append(line[0])
    Ram.append(line[1])
    Cpu.append(line[2])
    Peso.append(line[3])
    Robustez.append(line[4])
    Tiempo.append(line[5])

Gen = [int(e) for e in Gen[1:]]
Ram = [float(e) for e in Ram[1:]] if (float(Ram[1]) != -1.0) else []
Cpu = [float(e) for e in Cpu[1:]] if (float(Cpu[1]) != 1.0) else [] #Decidir si -1 o 1
Peso = [float(e) for e in Peso[1:]] if (float(Peso[1]) != -1.0) else []
Robustez = [float(e) for e in Robustez[1:]] if (float(Robustez[1]) != 1.0) else [] #Decidir si -1 o 1
Tiempo = [float(e) for e in Tiempo[1:]] if (float(Tiempo[1]) != -1.0) else []

if Gen:
    print(Gen)
if Ram:
    print(Ram)
    plot.gcf().set_size_inches(9, 5)
    plot.gcf().set_dpi(50)
    plot.plot(Gen, Ram, color='blue', marker='o')
    plot.title('Evolución del uso de la Ram')
    plot.xlabel('Generacion')
    plot.ylabel('Ram (MB)')
    plot.grid(True)
    plot.savefig('./charts/ram.png')
    plot.close()
if Cpu:
    print(Cpu)
    plot.gcf().set_size_inches(9, 5)
    plot.gcf().set_dpi(50)
    plot.plot(Gen, Cpu, color='blue', marker='o')
    plot.title('Evolución del consumo de la CPU')
    plot.xlabel('Generacion')
    plot.ylabel('%CPU')
    plot.savefig('./charts/cpu.png')
    plot.close()
if Peso:
    print(Peso)
    plot.gcf().set_size_inches(9, 5)
    plot.gcf().set_dpi(50)
    plot.plot(Gen, Peso, color='blue', marker='o')
    plot.title('Evolución del Peso del binario')
    plot.xlabel('Generacion')
    plot.ylabel('Peso en ??')
    plot.grid(True)
    plot.savefig('./charts/peso.png')
    plot.close()
if Robustez:
    print(Robustez)
    plot.gcf().set_size_inches(9, 5)
    plot.gcf().set_dpi(50)
    plot.plot(Gen, Robustez, color='blue', marker='o')
    plot.title('Evolución de porcentage de ejecuciones enmarcaradas')
    plot.xlabel('Generacion')
    plot.ylabel('Peso en ??')
    plot.grid(True)
    plot.savefig('./charts/robustez.png')
    plot.close()
if Tiempo:
    print(Tiempo)
    plot.gcf().set_size_inches(9, 5)
    plot.gcf().set_dpi(50)
    plot.plot(Gen, Tiempo, color='blue', marker='o')
    plot.title('Evolución de Tiempo de ejecución')
    plot.xlabel('Generación')
    plot.ylabel('Tiempo en segundos¿?')
    plot.grid(True)
    plot.savefig('./charts/tiempo.png')
    plot.close()


