import json
import flags

def inicializacionFlags(file):

    data = json.load(file)

    listaFlags = []
    for binarias in data['binarias']:
        nombre = str(binarias['flag'])
        objeto = flags.Flag(nombre)
        listaFlags.append(objeto)

    for rangos in data['rango']:
        nombre = str(rangos['flag'])
        minimo = int(rangos['min'])
        maximo = int(rangos['max'])
        objeto = flags.rangoFlag(nombre, minimo, maximo)
        listaFlags.append(objeto)

    for inter in data['Intervalo']:
        nombre = str(inter['flag'])
        intervalo = str(inter['intervalo']).split(',')
        objeto = flags.intervaloFLag(nombre, intervalo)
        listaFlags.append(objeto)

    return listaFlags


''' Prueba

flags = inicializacionFlags(open('../flags.json', 'r'))

for flag in flags:
    print(flag.getFlag())
'''
