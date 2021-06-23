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


for i in $(seq 1 $count)
do
    auxiliar=$(/usr/bin/time -f '%e' $BINARY $ARGS 2>&1 1>/dev/null);
    acumulador=$(echo $acumulador + $auxiliar | bc );
done

echo "scale=4; $acumulador / $count" | bc;