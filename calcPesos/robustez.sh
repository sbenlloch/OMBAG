#!/bin/bash
#Author: Sergio Benlloch, serbenl1
#Script to analyze the robustness of a binary
#[!]   Use:
#      -v or --verbose for activate comments
#      -b or -binary to pass binary to execute
#      -e or -executions to pass number of executions to zofi, default 50
#Zofi is needed for the execution of this script

VERBOSE=false
N=50
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
    esac
done

if [[ -x "$BINARY" ]]
then
    if [ "$VERBOSE" = true ]; then
    echo '[*]Running zofi with' $BINARY
    fi
else
    echo "File '$BINARY' is not executable or found"
    echo '[!]   Use:';
    echo '      -v or --verbose for activate comments';
    echo '      -b or -binary to pass binary to execute';
    echo '      -e or -executions to pass number of executions to zofi, default 50';
    exit;
fi

if [ -f /tmp/salidaZofi ]; then
    rm /tmp/salidaZofi;
fi

zofi -bin $BINARY -test-runs $N &>/tmp/salidaZofi;

if [ -f /tmp/salidaZofi ]; then

    if [ "$VERBOSE" = true ]; then
        echo '[*]Successfully executed';
        cat /tmp/salidaZofi | tail -n 7;
        exit;
    fi

    for element in $(cat /tmp/salidaZofi | tail -n 4 | awk '{print $4}' | cut -d \. -f 1)
    do
        echo "scale=2; $element/100" | bc | sed 's/^\./0./';
    done

else

    if [ "$VERBOSE" = true ]; then
        echo '[!]Executed with problems, Use:';
        echo '      -v or --verbose for activate comments';
        echo '      -b or -binary to pass binary to execute';
        echo '      -e or -executions to pass number of executions to zofi, default 50';
    fi

fi