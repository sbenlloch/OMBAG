import time


def comparacion(guardar):
    print('Se compara y ' + str(guardar))

def salidaFin(historico, directorioBase, Gen, limite, tiempo_inicio):
    print('\n\n\033[1;36m┌────────────────────────────────────────────────────────┐')
    print('│                  Ejecución finalizada                  │')
    print('└────────────────────────────────────────────────────────┘')
    if limite == 0:
        print(' Ejecución finalizada en ' + str(Gen) +' generaciones.\n')
    elif limite == 1:
        print(' Ejecución finalizada en ' + str(round(time.time() - tiempo_inicio, 1)) + ' segundos.\n')
    elif limite == 2:
        print(' Ejecución finalizada por convergencia ejecución.\n')
    else:
        print('Límite fuera de rango')

    print(' Se han generado automaticamente diferentes archivos de\n' +
        ' estadísticas de la ejecución, los puedes encontrar en la\n' +
        ' cartepa _Ejecucion12_04_2021-12:52:05 en el path que has\n' +
        ' configurado.\n')
    print(' Antes de finalizar:\n')
    comparar = input(' - ¿Quieres comparar el resultado con los flags de opti-\n   mización?[y/n]: ')
    if comparar == 'y':
        comparar=True
    else:
        comparar=False
    print('\n')
    if comparar:
        guardar = input(' - ¿Quieres guardar las estadísticas de comparación\n   anteriores en un archivo en el directorio configurado?\n   [y/n]: ')
        if guardar == 'y':
            guardar=True
        else:
            guardar=False
        print('\n')
    print('--------------------------------------------------------\n\n')
    print(' Esta es la línea de compilación seleccionada: \n')
    ultimoSeleccionado = sorted(historico[-1], key=lambda cromosoma: cromosoma.WSM)[0]
    lineaCompilacion = ultimoSeleccionado.lineaCompilacion
    lineaCompToVect = lineaCompilacion.split(' ')
    cont=0
    path = '<path programa>'
    for palabra in lineaCompToVect:
        if '/' in palabra:
            palabra = path
        if '-o' in palabra:
            path='<path ejecutable>'
        if cont == 2:
            print(' ' + palabra)
            cont = 0
        else:
            print(' ' + palabra, end='')
            cont+=1
    print('\n')
    if comparar:
        comparacion(guardar)