#!/usr/bin/env python3
import argparse
import serial
import time
from time import sleep
import datetime

def send_hold(ser, msg, duration=0, slp=0):
    now = datetime.datetime.now()
    print(f'[{now}] {msg}')
    ser.write(f'{msg}\r\n'.encode('utf-8'))
    sleep(duration)
    ser.write(b'HOLD_RE\r\n')
    sleep(slp)

def send(ser, msg, duration=0, slp=0):
    now = datetime.datetime.now()
    print(f'[{now}] {msg}')
    ser.write(f'{msg}\r\n'.encode('utf-8'))
    sleep(duration)
    ser.write(b'RELEASE\r\n')
    sleep(slp)

def league(ser):
    send_hold(ser, 'HOLD_LX 170', 0.1, 0)
    send_hold(ser, 'HOLD_LY MIN', 0.1, 0)
    while(True):
        send_hold(ser, 'Button A', 0.1, 0.3)
        send_hold(ser, 'Button A', 0.1, 0.3)
        send_hold(ser, 'Button A', 0.1, 0.3)
        send_hold(ser, 'Button A', 0.1, 0.3)
        send_hold(ser, 'Button A', 0.1, 0.4)
        send_hold(ser, 'Button B', 0.1, 0.4)
        send_hold(ser, 'Button A', 0.1, 0.3)
        send_hold(ser, 'Button A', 0.1, 0.3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("Start")
        send_hold(ser, 'Button R', 0.1, 0.1)
        send_hold(ser, 'Button L', 0.1, 0.1)
        league(ser)

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        ser.write(b'RELEASE\r\n')
        print("")
        print("End.")
        ser.close()
