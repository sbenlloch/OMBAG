#!/bin/bash
#Author: Sergio Benlloch, serbenl1
#Script to get the average, maximum and minimum use of the ram of an executable
#Data in
#Use:
#    -v or --verbose for activate comments';
#    -b or -binary to pass binary to execute';
#Mprof is needed for the execution of this script

calculo () {

    count=0;
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
        echo "scale=2; $total / $count" | bc;
        echo $max;
        echo $min;
    fi

}

VERBOSE=false

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
    esac
done

if [[ -x "$BINARY" ]]
then
    if [ "$VERBOSE" = true ]; then
    echo '[*]Running mprof with' $BINARY
    fi
else
    echo "File '$BINARY' is not executable or found"
    echo '[!]   Use:';
    echo '      -v or --verbose for activate comments';
    echo '      -b or -binary to pass binary to execute';
    exit;
fi

if [ -f /tmp/salidaMprof ]; then
    rm /tmp/salidaMprof;
fi

mprof run --output /tmp/salidaMprof $BINARY &>/dev/null

if [ -f /tmp/salidaMprof ]; then

    if [ "$VERBOSE" = true ]; then
        echo '[*]Successfully executed';
    fi

    salidaInVar=$( cat /tmp/salidaMprof | awk -v var=val '{print $3}');
    calculo;

else

    if [ "$VERBOSE" = true ]; then
        echo '[!]Executed with problems, Use:';
        echo '      -v or --verbose for activate comments';
        echo '      -b or -binary to pass binary to execute';
    fi

fi