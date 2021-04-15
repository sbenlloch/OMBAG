#!/bin/bash
#This script pretends to return user time of execution in ns
#Only with one number for do more practice utilization of other algorithms
#
#Author: Sergio Benllo, sg1o
#Version: 0.1


TIMEFORMAT=%U
time $1 &>/dev/null