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

def tower(ser):
    while(True):
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'Button A', 0.1, 15) # 0.8-14=32=29.5 # 0.8-15=30.2
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'LY MIN',   0.1, 0.8)
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'LY MIN',   0.1, 0.8)
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'Button A', 0.1, 15)
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'Button A', 0.1, 0.8)
        send(ser, 'Button B', 0.1, 0.8)
        send(ser, 'Button B', 0.1, 0.8)
        send(ser, 'LY MIN',   0.1, 0.8)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("Start")
        send(ser, 'Button B', 0.1, 0.5)
        send(ser, 'Button A', 0.1, 0.5)
        tower(ser)

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        print("")
        print("End.")
        ser.close()
