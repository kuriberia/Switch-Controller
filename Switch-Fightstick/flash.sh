#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Please input file name."
else
    echo "Start"
    echo ""
    echo "- dfu-programmer.exe ATmega16U2 erase"
    ./dfu-programmer.exe ATmega16U2 erase
    echo "- dfu-programmer.exe ATmega16U2 flash ${1}.hex"
    ./dfu-programmer.exe ATmega16U2 flash ${1}.hex
    echo "- dfu-programmer.exe ATmega16U2 reset"
    ./dfu-programmer.exe ATmega16U2 reset
    echo ""
    echo "End."
fi