#!/usr/bin/env python3
import argparse
import serial
import time
from time import sleep
import datetime

def send(ser, msg, duration=0, slp=0):
    now = datetime.datetime.now()
    # print(f'[{now}] {msg}')
    ser.write(f'{msg}\r\n'.encode('utf-8'))
    sleep(duration)
    ser.write(b'RELEASE\r\n')
    sleep(slp)

def shohi(ser, num=0):
    cnt = 0
    day = 1
    while(cnt < num):
        send(ser, 'Button A', 0.1, 0.11)
        send(ser, 'LX MIN',   0.05, 0.04)
        send(ser, 'LX MIN',   0.05, 0.04)
        send(ser, 'LX MIN',   0.05, 0.04)
        send(ser, 'LY MIN',   0.05, 0.04) # 1日進める
        send(ser, 'LX MAX',   0.05, 0.04)
        send(ser, 'LX MAX',   0.05, 0.04)
        send(ser, 'LX MAX',   0.05, 0.04)
        send(ser, 'Button A', 0.1, 0.11) # OK
        day += 1
        if(day == 32):
            day = 1
            print("Count :", cnt)
        else:
            cnt += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("月を31日ある月にあわせ、日を1日にしてください.")
        print("消費回数を入力 > ", end="")
        num = int(input())
        print(num, "回消費します．よろしいですか？ y or n > ", end="")
        str = input()
        if(str == "y"):
            send(ser, 'LY MAX',   0.1, 0.1)
            shohi(ser, num)
        else:
            print("終了します.")

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        print("Count :", cnt)
        ser.close()
