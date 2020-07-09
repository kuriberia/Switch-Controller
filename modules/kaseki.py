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

def kaseki(ser, num=1):
    cnt = 0
    while(cnt < num):
        send(ser, 'Button A', 0.1, 0.6)
        send(ser, 'Button A', 0.1, 0.7)
        send(ser, 'Button A', 0.1, 0.7)
        send(ser, 'Button A', 0.1, 0.7)
        send(ser, 'Button A', 0.1, 0.5)
        send(ser, 'Button A', 0.1, 3.7)
        send(ser, 'Button A', 0.1, 0.6)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 4.1)
        send(ser, 'Button A', 0.1, 1.5)
        send(ser, 'Button A', 0.1, 1.4)
        cnt += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("Start...")
        print("掘る回数 > ", end="")
        num = int(input())
        send(ser, 'Button R', 0.1, 0.5)
        send(ser, 'Button L', 0.1, 0.5)
        kaseki(ser, num)

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        print("")
        print("End.")
        ser.close()
