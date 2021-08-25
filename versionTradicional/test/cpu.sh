#!/bin/bash
#Author: Sergio Benlloch, serbenl1
#This script returns the cpu usage by an executable
#Use:
# -v or --verbose for activate comments
# -b or -binary to pass binary to execute
#-t or -time to pass interval to pidstat, default 2
#-a or --arguments to pass arguments, if there is more than one argument pass between quotes
#Example os Use:
# ./cpu.sh -b <EXECUTABLE> -t 1 -a <ARGUMENTS>
#./cpu.sh -b /usr/bin/seq -t 1 -a '1 10000000'
#pidstat is needed for the execution of this script
#In time:
#P      Percentage of the CPU that this job got.  This is just user + system times divided by the
#       total running time.  It also prints a percentage sign.
#[!]In short programs this test fails


VERBOSE=false
N=2
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
        -t|--time)
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
        echo '[*]Running pidstat with' $BINARY
    fi
else
    echo "File '$BINARY' not executable or not found"
    echo '[!]   Use:';
    echo '      -v or --verbose for activate comments';
    echo "      -b or -binary to pass binary to execute, If there are arguments pass as follows: '/path/to/binary <ARGS>'"
    echo "      -t or -time to pass interval to pidstat, default 2"
    echo "      -a or --arguments to pass arguments, if there is more than one argument pass between quotes"
    echo "Example os Use:"
    echo "  ./cpu.sh -b <EXECUTABLE> -t 1 -a <ARGUMENTS>"
    echo "  ./cpu.sh -b /usr/bin/seq -t 1 -a '1 10000000'"
    exit;
fi

to_execute=$BINARY

if [ "$ARGS" != "" ]; then
    to_execute=$to_execute' '$ARGS
fi

archivo=/tmp/salidaCPU$RANDOM$RANDOM

pidstat $N -u -e $to_execute > $archivo;

if [ -f $archivo ]; then

    if [ "$VERBOSE" = true ]; then
        echo '[*]Successfully executed';
    fi

    avg=$(cat $archivo | grep Average: | awk '{print $8}' | tail -1 | tr ',' '.');

    if [ "$avg" ]; then

        if [ "$VERBOSE" = true ]; then
            echo "scale=4; $avg/100" | bc | sed 's/^\./0./';
        fi
        echo "scale=4; $avg/100" | bc | sed 's/^\./0./';


    else

        avg=$(/usr/bin/time -f '%P' $to_execute 2>&1 1>/dev/null)
        avg2=$( echo $avg | sed 's/%//' );
        if [ $avg2=='?' ]; then
            avg2=100
        fi
        if [ "$VERBOSE" = true ]; then
            echo -n "AVG CPU: ";
            echo "scale=4; $avg2/100" | bc | sed 's/^\./0./';
        fi
        echo "scale=4; $avg2/100" | bc | sed 's/^\./0./';

    fi

else

    if [ "$VERBOSE" = true ]; then
        echo '[!]Executed with problems, Use:';
        echo '      -v or --verbose for activate comments';
        echo "      -b or -binary to pass binary to execute, If there are arguments pass as follows: '/path/to/binary <ARGS>'"
        echo "      -t or -time to pass interval to pidstat, default 2"
        echo "      -a or --arguments to pass arguments, if there is more than one argument pass between quotes"
        echo "Example os Use:"
        echo "  ./cpu.sh -b <EXECUTABLE> -t 1 -a <ARGUMENTS>"
        echo "  ./cpu.sh -b /usr/bin/seq -t 1 -a '1 10000000'"
    fi

fi

if [ -f $archivo ]; then
    rm $archivo;
fi