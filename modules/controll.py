#!/usr/bin/env python3
import argparse
import serial
import time
from time import sleep
import datetime

def send(ser, msg, duration=0, slp=0):
    now = datetime.datetime.now()
    print(f'[{now}] {msg}')
    ser.write(f'{msg}\r\n'.encode('utf-8'))
    sleep(duration)
    ser.write(b'RELEASE\r\n')
    sleep(slp)

def send_cmd(ser, str):
    if str == "a" or str == "":
        send(ser, 'Button A', 0.1, 0.1)
    elif str == "b":
        send(ser, 'Button B', 0.1, 0.1)
    elif str == "x":
        send(ser, 'Button X', 0.1, 0.1)
    elif str == "y":
        send(ser, 'Button Y', 0.1, 0.1)
    elif str == "l1":
        send(ser, 'Button L', 0.1, 0.1)
    elif str == "r1" or str == "z":
        send(ser, 'Button R', 0.1, 0.1)
    elif str == "h":
        send(ser, 'Button HOME', 0.1, 0.1)
    elif str == 'p':
        send(ser, 'Button START', 0.1, 0.1)
    elif str == 'm':
        send(ser, 'Button SELECT', 0.1, 0.1)
    elif str == "r":
        send(ser, 'LX MAX',   0.2, 0.1)
    elif str == "l":
        send(ser, 'LX MIN',   0.2, 0.1)
    elif str == "u":
        send(ser, 'LY MIN',   0.2, 0.1)
    elif str == "d":
        send(ser, 'LY MAX',   0.2, 0.1)
    else:
        print("unkown command.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        flag = True
        while(flag):
            print("> ", end="")
            str = input()
            if(str == "end" or str == "exit" or str == ";"):
                flag = False
            else:
                send_cmd(ser, str)

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        print("End.")
        ser.close()
