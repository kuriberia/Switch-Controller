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

def restart(ser):
    send(ser, 'Button HOME', 0.1, 0.6)
    send(ser, 'Button X', 0.1, 0.3)
    send(ser, 'Button A', 0.1, 2.6)
    send(ser, 'Button A', 0.1, 13.7)
    send(ser, 'Button A', 0.1, 7.0)
    print("End")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("Start")
        send(ser, 'Button R', 0.1, 0.4)
        send(ser, 'Button L', 0.1, 0.4)
        send(ser, 'Button R', 0.1, 0.4)
        restart(ser)

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        ser.close()
