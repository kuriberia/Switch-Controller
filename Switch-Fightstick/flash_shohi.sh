#!/bin/bash
echo "Start"
echo ""
echo "- dfu-programmer.exe ATmega16U2 erase"
./dfu-programmer.exe ATmega16U2 erase
echo "- dfu-programmer.exe ATmega16U2 flash shohi.hex"
./dfu-programmer.exe ATmega16U2 flash shohi.hex
echo "- dfu-programmer.exe ATmega16U2 reset"
./dfu-programmer.exe ATmega16U2 reset
echo ""
echo "End."
