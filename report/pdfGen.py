from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
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
pdf.setTitle(nombre_archivo)
pdf.setFont('Courier', 20)
pdf.drawCentredString(300, 770, 'Reporte resultados')
pdf.drawCentredString(305, 750, 'optimización de compilados')
pdf.line(45, 740, 535, 740)
Intro = ['En este reporte encontrarás los resultados de la optimización graficamente,',
        'en cada apartado encontrarás una gráfica y un pequeño resumen de cada parte']
text = pdf.beginText(50, 710)
text.setFont('Helvetica', 13)
for line in Intro:
    text.textLine(line)
pdf.drawText(text)

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
Cpu = [float(e) for e in Cpu[1:]] if (float(Cpu[1]) != -1.0) else [] #Decidir si -1 o 1
Peso = [float(e) for e in Peso[1:]] if (float(Peso[1]) != -1.0) else []
Robustez = [float(e) for e in Robustez[1:]] if (float(Robustez[1]) != 1.0) else [] #Decidir si -1 o 1
Tiempo = [float(e) for e in Tiempo[1:]] if (float(Tiempo[1]) != -1.0) else []
H = 50
W = 660
if Ram:
    plot.gcf().set_size_inches(8, 6)
    plot.gcf().set_dpi(300)
    plot.plot(Gen, Ram, color='blue', marker='o')
    plot.title('Evolución del uso de la Ram')
    plot.xlabel('Generación')
    plot.ylabel('Ram (MB)')
    plot.grid(True)
    plot.savefig('./charts/ram.png')
    plot.close()
    pdf.showPage()
    W = 770
    W -= 20
    pdf.setFont('Helvetica', 18)
    pdf.drawString(H, W, 'Resultados consumo memoria RAM del binario')
    cuerpoPeso = ["En este apartado tenemos los resultados de la evolución del binerio, este caso",
                "vemos el peso en MB en el 'eje y' y la evolución en cada generación en el eje x"]
    W -= 20
    text = pdf.beginText(H, W)
    text.setFont('Helvetica', 13)
    for line in cuerpoPeso:
        text.textLine(line)
    pdf.drawText(text)
    W -= 375
    pdf.drawInlineImage('./charts/ram.png', 40, W, 520, 350)
if Cpu:
    plot.gcf().set_size_inches(8, 6)
    plot.gcf().set_dpi(300)
    plot.plot(Gen, Cpu, color='blue', marker='o')
    plot.title('Evolución del consumo de la CPU')
    plot.xlabel('Generación')
    plot.ylabel('% CPU')
    plot.savefig('./charts/cpu.png')
    plot.close()
    pdf.showPage()
    W = 770
    W -= 20
    pdf.setFont('Helvetica', 18)
    pdf.drawString(H, W, 'Resultados consumo de CPU del binario')
    cuerpoPeso = ["En este apartado tenemos los resultados de la evolución del binerio, este caso",
                "vemos el peso en MB en el 'eje y' y la evolución en cada generación en el eje x"]
    W -= 20
    text = pdf.beginText(H, W)
    text.setFont('Helvetica', 13)
    for line in cuerpoPeso:
        text.textLine(line)
    pdf.drawText(text)
    W -= 375
    pdf.drawInlineImage('./charts/cpu.png', 40, W, 520, 350)
if Peso:
    plot.gcf().set_size_inches(8, 6)
    plot.gcf().set_dpi(300)
    plot.plot(Gen, Peso, color='blue', marker='o')
    plot.title('Evolución del Peso del binario')
    plot.xlabel('Generación')
    plot.ylabel('Peso en ??')
    plot.grid(True)
    plot.savefig('./charts/peso.png')
    plot.close()
    pdf.showPage()
    W = 770
    pdf.setFont('Helvetica', 18)
    pdf.drawString(H, W, 'Resultados peso del binario')
    cuerpoPeso = ["En este apartado tenemos los resultados de la evolución del binario, este caso",
                "vemos el peso en MB en el 'eje y' y la evolución en cada generación en el eje x"]
    W -= 20
    text = pdf.beginText(H, W)
    text.setFont('Helvetica', 13)
    for line in cuerpoPeso:
        text.textLine(line)
    pdf.drawText(text)
    W -= 375
    pdf.drawInlineImage('./charts/peso.png', 40, W, 520, 350)
if Robustez:
    plot.gcf().set_size_inches(8, 6)
    plot.gcf().set_dpi(300)
    plot.plot(Gen, Robustez, color='blue', marker='o')
    plot.title('Evolución de porcentage de ejecuciones enmascaradas')
    plot.xlabel('Generación')
    plot.ylabel('Robustez')
    plot.grid(True)
    plot.savefig('./charts/robustez.png')
    plot.close()
    pdf.showPage()
    W = 770
    W -= 20
    pdf.setFont('Helvetica', 18)
    pdf.drawString(H, W, 'Resultados robustez del binario')
    cuerpoPeso = ["En este apartado tenemos los resultados de la evolución del binario, este caso",
                "vemos el peso en MB en el 'eje y' y la evolución en cada generación en el eje x"]
    W -= 20
    text = pdf.beginText(H, W)
    text.setFont('Helvetica', 13)
    for line in cuerpoPeso:
        text.textLine(line)
    pdf.drawText(text)
    W -= 375
    pdf.drawInlineImage('./charts/robustez.png', 40, W, 520, 350)
if Tiempo:
    plot.gcf().set_size_inches(8, 6)
    plot.gcf().set_dpi(300)
    plot.plot(Gen, Tiempo, color='blue', marker='o')
    plot.title('Evolución de Tiempo de ejecución')
    plot.xlabel('Generación')
    plot.ylabel('Tiempo en segundos¿?')
    plot.grid(True)
    plot.savefig('./charts/tiempo.png')
    plot.close()
    pdf.showPage()
    W = 770
    W -= 20
    pdf.setFont('Helvetica', 18)
    pdf.drawString(H, W, 'Resultados tiempo ejecución del binario')
    cuerpoPeso = ["En este apartado tenemos los resultados de la evolución del tiempo de ejecución,",
                "este caso vemos el tiempo en segundos en el 'eje y' y la evolución en el eje x"]
    W -= 20
    text = pdf.beginText(H, W)
    text.setFont('Helvetica', 13)
    for line in cuerpoPeso:
        text.textLine(line)
    pdf.drawText(text)
    W -= 375
    pdf.drawInlineImage('./charts/tiempo.png', 40, W, 520, 350)


pdf.save()