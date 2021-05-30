#!/bin/bash
#Author: Sergio Benlloch, serbenl1
#Script to analyze the robustness of a binary
#[!]   Use:
#      -v or --verbose for activate comments
#      -b or -binary to pass binary to execute
#      -e or -executions to pass number of executions to zofi, default 50
#      -a or --arguments for pass arguments, if there is more than one argument pass between quotes
#Zofi is needed for the execution of this script

VERBOSE=false
N=50
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
        -e|--executions)
        N=$2
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

if [[ -x "$BINARY" ]]
then
    if [ "$VERBOSE" = true ]; then
    echo '[*]Running zofi with' $BINARY
    fi
else
    echo "File '$BINARY' not executable or not found"
    echo '[!]   Use:';
    echo '      -v or --verbose for activate comments';
    echo '      -b or --binary to pass binary to execute';
    echo '      -e or --executions to pass number of executions to zofi, default 50';
    echo "      -a or --arguments for pass arguments, if there is more than one argument pass between quotes "
    exit;
fi

archivo=/tmp/salidaCPU$RANDOM$RANDOM

zofi -bin $BINARY -test-runs $N -args $ARGS &>/$archivo;

if [ -f $archivo ]; then

    if [ "$VERBOSE" = true ]; then
        echo '[*]Successfully executed';
        cat $archivo | tail -n 7;
        exit;
    fi

    for element in $(cat $archivo | tail -n 4 | awk '{print $4}' | cut -d \. -f 1)
    do
        echo "scale=2; $element/100" | bc | sed 's/^\./0./';
    done

else

    if [ "$VERBOSE" = true ]; then
        echo '[!]Executed with problems, Use:';
        echo '      -v or --verbose for activate comments';
        echo '      -b or --binary to pass binary to execute';
        echo '      -e or --executions to pass number of executions to zofi, default 50';
        echo "      -a or --arguments for pass arguments, if there is more than one argument pass between quotes "
    fi

fi

if [ -f $archivo ]; then
    rm $archivo;
fi