#!/bin/bash
#This script pretends to return user size of program in bytes
#Only with one number for do more practice utilization of other algorithms
#
#Author: Sergio Benllo, sg1o
#Version: 0.1

du -b $1 | awk '{print $1}'