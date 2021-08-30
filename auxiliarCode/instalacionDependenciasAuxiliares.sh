#!/bin/bash
#Script creado por sg10, Sergio Benlloch
#Este script incluye la instalación de las dependencias necesarias
#para ejecutar lor programas auxiliares, es necesario haber instalado las dependencias
#de los programas de optimización

echo '[!]Para ejecutar este script debes tener instalado las dependencias de los programas de optimización'
echo ''
echo '[*]Instalando Matplotlib'
plot=$(pip list 2>/dev/null | grep matplotlib)

if [ "$plot" ]
    then
        echo "[!] Matplotlib satisfecho"
    else
        echo "[!]Matplotlib no satisfecho, se va a instalar"
	sudo pip install matplotlib &>/dev/null
fi
echo ''
echo '[*]Instalando Numpy'
mumpy=$(pip list 2>/dev/null | grep numpy)

if [ "$numpy" ]
    then
        echo "[!] Numpy satisfecho"
    else
        echo "[!]Numpy no satisfecho, se va a instalar"
	sudo pip install numpy &>/dev/null
fi