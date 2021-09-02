# (EN CONSTRUCCIÓN) OMBAG: Optimización Multiobjetivo de Binarios con Algoritmos Genéticos

En este repositorio encontrarás una implementación de un Algoritmo Genético para optimizar respecto a varios objetivos la compilación de binarios usando las flags de GCC.

Puedes encontrar una versión de un Algoritmo genético tradicional y una solución siguiendo Modelo de Islas.

## Instalación ⏳

Ambas versiones de los algoritmos están implementadas en Python 3, no usan módulos externos y no tienen dependencias de código, pero, para la medición de cada individuo es necesario tener instalado algunas aplicaciones. 

Todas las aplicaciones son compatibles con sistemas basados en Debian, testeadas en Ubuntu 20.04 LTS y Ubuntu Server 20.04.3 LTS.

Para instalar las dependencias cuentas con un script de instalación. Puedes instalarlo ejecutando:

```bash
> sudo ./instalacion.sh
> sudo ./auxiliarCode/instalacionDependenciasAuxiliares.sh
```

Una vez instaladas las dependencias ya puedes ejecutar los algoritmos genéticos.

## Uso Algoritmo Genético 📚

 Para hacer uso de cualquier versión los algoritmos genéticos puedes seguir los siguientes pasos:

 ### Configuración ⚙️


Cuentas con un archivo de configuración, _conf.ini_, donde puedes configurar parámetros como tamaño de población o pesos de los objetivos a optimizar.

### Ejecución 🚀

Para lanzar a ejecución puedes usar la siguiente orden:

```bash
> python3 optimize.py -p path/al/binario [ -a <ARGS> ]
```

Donde _-p_ indica el path del programa a ejecutar y si los tiene con  _-a_ puedes indicar los argumentos.

También existen otros parámetros:

```bash
-p : + path del programa
-a : + argumentos del programa
-dF: Modo depuración de la compilación
-i : Modo impresión de resultados durante ejecución
```
### Salida 📖

# Construido con 💻🖱️⌨️🛠️

# Autor 🪐🚀

🔗 GitHub : [sgio](http://github.com/sgio)


# Licencia 📄

GPL 3.0

