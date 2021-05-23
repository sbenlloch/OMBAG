#!/bin/bash
#Author: Sergio Benlloch, serbenl1
#Script to measure the cpu usage of an executable
#Use:
# -v or --verbose for activate comments
# -b or -binary to pass binary to execute
#-t or -time to pass interval to pidstat, default 2
#pidstat is needed for the execution of this script

VERBOSE=false
N=2
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
        -t|--time)
        N=$2
        shift
        shift
        ;;
    esac
done

if [[ -x "$BINARY" ]]
then
    if [ "$VERBOSE" = true ]; then
    echo '[*]Running pidstat with' $BINARY
    fi
else
    echo "File '$BINARY' is not executable or found"
    echo '[!]   Use:';
    echo '      -v or --verbose for activate comments';
    echo '      -b or -binary to pass binary to execute';
    echo '      -t or -time to pass interval to pidstat, default 2';
    exit;
fi

if [ -f /tmp/salidaCPU ]; then
    rm /tmp/salidaCPU;
fi

pidstat $N -u -e $BINARY > /tmp/salidaCPU;

if [ -f /tmp/salidaCPU ]; then

    if [ "$VERBOSE" = true ]; then
        echo '[*]Successfully executed';
    fi

    all=$(cat /tmp/salidaCPU | awk '{print $8}' | head --lines=-3 | tail --lines=+2);

    if [ "$all" ]; then

        avg=$(cat /tmp/salidaCPU | grep Average: | awk '{print $8}' | tail -1 | tr ',' '.');
        if [ "$VERBOSE" = true ]; then
            echo "scale=4; $avg/100" | bc | sed 's/^\./0./';
            exit;
            exit;
        fi
        echo "scale=4; $avg/100" | bc | sed 's/^\./0./';
        exit;

    else

        /usr/bin/time -o /tmp/salidaCPU -v $BINARY &>/dev/null;
        avg=$( cat /tmp/salidaCPU | head -4 | tail -1 | awk '{print $7}' );
        avg2=$( echo $avg | sed 's/%//' );
        if [ "$VERBOSE" = true ]; then
            echo -n "AVG CPU: ";
            echo "scale=4; $avg2/100" | bc | sed 's/^\./0./';
            exit;
        fi
        echo "scale=4; $avg2/100" | bc | sed 's/^\./0./';

    fi

else

    if [ "$VERBOSE" = true ]; then
        echo '[!]Executed with problems, Use:';
        echo '      -v or --verbose for activate comments';
        echo '      -b or -binary to pass binary to execute';
        echo '      -t or -time to pass interval to pidstat, default 2';
    fi

fi