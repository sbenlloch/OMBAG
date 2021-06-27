import time

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
    copia = input(' - ¿Quieres copiar el archivo del compilado final a\n   este directorio?[y/n]: ')
    print('\n')
    comparar = input(' - ¿Quieres comparar el resultado con los flags de opti-\n   mización por defecto de GCC en cada uno de los objeti-\n   vos?[y/n]: ')
    print('\n')
    guardar = input(' - ¿Quieres guardar las estadísticas de comparación\n   anteriores en un archivo en el directorio seleccionado?\n   [y/n]: ')
    print('\n')
    print('--------------------------------------------------------')