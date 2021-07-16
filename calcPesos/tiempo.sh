#!/bin/bash
#This script pretends to return user time of execution in seconds
#Only with one number for do more practice utilization of other algorithms
#
#Author: Sergio Benlloch, sg1o
#Version: 0.1
#For pass arguments: ./time.sh -b <BINARY> -a '<ARGS>' -e <Number of executions>

acumulador=0
count=10
ARGS=''
for arg in "$@"
do
    case $arg in
        -b|--binary)
        BINARY=$2
        shift
        shift
        ;;
        -a|--arguments)
        ARGS=$2
        shift
        shift
        ;;
        -e|--executions)
        count=$2
        shift
        shift
    esac
done

minimo=$(/usr/bin/time -f '%e' $BINARY $ARGS 2>&1 1>/dev/null)

for i in $(seq 2 $count)
do
    auxiliar=$(/usr/bin/time -f '%e' $BINARY $ARGS 2>&1 1>/dev/null);
    if (( $(echo "$minimo > $auxiliar" | bc -l) )); then
            minimo=$auxiliar;
    fi
done

echo $minimo;