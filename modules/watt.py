#!/usr/bin/env python3
import argparse
import serial
import time
from time import sleep
import datetime

import idkuji

def send(ser, msg, duration=0, slp=0):
    now = datetime.datetime.now()
    print(f'[{now}] {msg}')
    ser.write(f'{msg}\r\n'.encode('utf-8'))
    sleep(duration)
    ser.write(b'RELEASE\r\n')
    sleep(slp)

def watt(ser):
    while(True):
        idkuji.year(ser)
        send(ser, 'Button A', 0.1, 0.3) # ワット回収 「巣穴からエネルギーが少しだけでている！▼」
        send(ser, 'Button B', 0.1, 0.3) # 「シベリアは1000W手に入れた！▼」
        send(ser, 'Button B', 0.1, 1.0) # レイドが開く
        send(ser, 'Button B', 0.1, 1.0) # レイド閉じる

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("Start")
        send(ser, 'Button B', 0.1, 0.2)
        send(ser, 'Button B', 0.1, 0.5)
        watt(ser)

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        print("End.")
        ser.close()
