#!/usr/bin/env python3
import argparse
import serial
import time
from time import sleep
import datetime

import day4raid

def send(ser, msg, duration=0, slp=0):
    now = datetime.datetime.now()
    print(f'[{now}] {msg}')
    ser.write(f'{msg}\r\n'.encode('utf-8'))
    sleep(duration)
    ser.write(b'RELEASE\r\n')
    sleep(slp)

def days(ser, num=1):
    cnt = 0
    while(cnt < num):
        day4raid.day(ser)
        cnt += 1
        print("")
        print(cnt, "day")
        print("")

    send(ser, 'Button A', 0.1, 1.0)
    send(ser, 'LY MAX',   0.1, 0.3)
    print("End.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    parser.add_argument('-d', '--day', type=int, default=3)
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("Start...")
        send(ser, 'Button B', 0.1, 0.2)
        send(ser, 'Button B', 0.1, 0.5)
        print("day :", args.day)
        days(ser, args.day)

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        print("End.")
        ser.close()
