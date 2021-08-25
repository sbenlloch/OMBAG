#!/bin/bash
#Author: Sergio Benlloch, serbenl1
#Script to get the average, maximum and minimum use of the ram of an executable
#Data in
#Use:
#    -v or --verbose for activate comments
#    -b or -binary to pass binary to execute
#    -a or --arguments to pass arguments, if there is more than one argument pass between quotes
#Example of use:
#  ./ram.sh -b /usr/bin/seq -a '1 1000000000'
#Mprof is needed for the execution of this script, output data in MB

calculo () {

    count=0;#revisar division por 0
    total=0;
    max=0;
    min=$( echo $salidaInVar | awk '{print $1}' );

    for elemento in $(echo $salidaInVar)
    do
        total=$(echo $total + $elemento | bc );
        ((count++));

        if (( $(echo "$elemento > $max" |bc -l) )); then
            max=$elemento;
        fi

        if (( $(echo "$min > $elemento" |bc -l) )); then
            min=$elemento;
        fi
    done

    if [ "$VERBOSE" = true ]; then
        echo -n "Avg: ";
        echo "scale=4; $total / $count" | bc;
        echo 'Max:' $max;
        echo 'Min:' $min;
    else
        #echo "scale=2; $total / $count" | bc;
        echo $max;
        #echo $min;
    fi
}

VERBOSE=false
ARGS=''
for arg in "$@"
do
    case $arg in
        -v|--verbose)
        VERBOSE=true
        shift
        ;;
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
    esac
done

if [[ -x "$BINARY" ]]; then
    if [ "$VERBOSE" = true ]; then
        echo '[*]Running mprof with' $BINARY
    fi
else
    echo "File '$BINARY' not executable or not found"
    echo '[!]   Use:';
    echo '      -v or --verbose for activate comments;'
    echo "      -b or -binary to pass binary to execute"
    echo '      -a or --arguments to pass arguments, if there is more than one argument pass between quotes'
    echo 'Example of use:'
    echo " ./ram.sh -b /usr/bin/seq -a '1 1000000000'"
    exit;
fi

to_execute=$BINARY

if [ "$ARGS" != "" ]; then
    to_execute=$to_execute' '$ARGS
fi

output=/tmp/salidaMprof$RANDOM$RANDOM

mprof run --output $output $to_execute &>/dev/null

if [ -f $output ]; then

    if [ "$VERBOSE" = true ]; then
        echo '[*]Successfully executed';
    fi

    salidaInVar=$( tail -n +2 $output | awk '{print $2}');
    calculo;

else

    if [ "$VERBOSE" = true ]; then
        echo '[!]Executed with problems, Use:';
        echo '      -v or --verbose for activate comments';
        echo "      -b or -binary to pass binary to execute";
        echo '      -a or --arguments to pass arguments, if there is more than one argument pass between quotes'
        echo 'Example of use:'
        echo " ./ram.sh -b /usr/bin/seq -a '1 1000000000'"
    fi

fi

if [ -f $output ]; then
    rm $output;
fi
