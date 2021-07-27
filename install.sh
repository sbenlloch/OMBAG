#!/bin/bash
#Script creado por sg10, Sergio Benlloch
#Este script incluye la instalación de las dependencias necesarias
#para ejecutar las pruebas del algoritmo genético.
#Este script esta testado en Ubuntu 20.04 LTS y Ubuntu Server 20.04 LTS Gen 2


printf "[*]Instalación de Prerequisitos\n"

gcc='gcc'

dpkg -s $gcc &> /dev/null

if [ $? -ne 0 ]
    then
        echo "[!]GCC no satisfecho, se va a instalar"
        sudo apt-get install $gcc -y &>/dev/null
        dpkg -s $gcc &> /dev/null && echo "[*]GCC instalado exitosamente"

    else
        echo "[!]GCC satisfecho"
fi

make='make'

dpkg -s $make &> /dev/null

if [ $? -ne 0 ]
    then
        echo "[!]Make no satisfecho, se va a instalar"
        sudo apt-get install $make -y &>/dev/null
        dpkg -s $make &> /dev/null && echo "[*]Make instalado exitosamente"

    else
        echo "[!]Make satisfecho"

fi

git='git'

dpkg -s $git &> /dev/null

if [ $? -ne 0 ]
    then
        echo "[!]Git no satisfecho, se va a instalar"
        sudo apt-get install $git -y &>/dev/null
        dpkg -s $git &> /dev/null && echo "[*]Git instalado exitosamente"

    else
        echo "[!]Git satisfecho"

fi


#################################################################

printf "[*]Instalación de dependencias para medir Carga de CPU\n"

stat='sysstat'

dpkg -s $stat &> /dev/null

if [ $? -ne 0 ]
    then
        echo "[!]Sysstat no satisfecho, se va a instalar"
        sudo apt-get install $stat -y &>/dev/null
        dpkg -s $stat &> /dev/null && echo "[*]Sysstat instalado exitosamente"

    else
        echo "[!]Sysstat satisfecho"

fi

###############################################################

printf "[*]Instalación de dependencias para medir uso de RAM\n"

pip='python3-pip'

dpkg -s $pip &> /dev/null

if [ $? -ne 0 ]
    then
        echo "[!]PIP no satisfecho, se va a instalar"
        sudo apt-get install $pip -y &>/dev/null
        dpkg -s $pip &> /dev/null && echo "[*]PIP instalado exitosamente"

    else
        echo "[!]PIP satisfecho"

fi

mprof=$(pip list | grep memory-profiler)

if [ "$mprof" ]
    then
        echo "[!] MPROF satisfecho"
    else
        echo "[!]MPROF no satisfecho, se va a instalar"
	pip install memory-profiler &>/dev/null
	sudo cp ~/.local/bin/mprof /usr/bin/
fi


###############################################################

printf "[*]Instalación de dependencias para medir Robustez\n"

echo "[!]Capstone 4.0.1 no satisfecho, se va a instalar"
wget https://github.com/aquynh/capstone/archive/4.0.1.tar.gz &>/dev/null
tar -xvf 4.0.1.tar.gz &>/dev/null
cd capstone-4.0.1/  &>/dev/null && ./make.sh &>/dev/null && sudo make install &>/dev/null
sudo ldconfig &>/dev/null
cd ..
rm 4.0.1.tar.gz
rm -rf capstone-4.0.1/

###

echo "[!]Zofi no satisfecho, se va a instalar"
git clone https://github.com/vporpo/zofi &>/dev/null
cd zofi
mkdir build &>/dev/null && cd build &>/dev/null

cmake='cmake'

dpkg -s $cmake &> /dev/null

if [ $? -ne 0 ]
    then
        echo "[!]Cmake no satisfecho, se va a instalar"
        sudo apt-get install $cmake -y &>/dev/null
        dpkg -s $cmake &> /dev/null && echo "[*]Cmake instalado exitosamente"

    else
        echo "[!]Cmake satisfecho"

fi

cmake ../src/ &>/dev/null && make -j &>/dev/null && sudo make install &>/dev/null
cd ../..
rm -rf zofi/

