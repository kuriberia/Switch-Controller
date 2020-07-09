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

def pokejob(ser, poke=1, day=1):
    cnt = 0
    while(cnt < day):
        send(ser, 'Button A', 0.1, 0.2) # ロトミにアクセス
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'Button A', 0.1, 2.8) # ポケジョブを開く
        send(ser, 'Button A', 0.1, 0.2)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 1.1)
        send(ser, 'Button Y', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3) # ポケモンを選ぶ
        for _ in range(1, poke):
            send(ser, 'LX MAX',   0.1, 0.1)
            send(ser, 'Button A', 0.1, 0.1) # ポケモンを選ぶ
        send(ser, 'Button B', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 2.1)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3)
        print("いってらっしゃいムービー")
        send(ser, 'Button A', 0.1, 9.5) # 1日で送り出す
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button B', 0.1, 0.6)
        send(ser, 'Button A', 0.1, 0.3)

        print("時渡り")
        send(ser, 'Button HOME', 0.1, 0.5) # ホームに戻る
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'Button A', 0.1, 0.2) # 設定を開く
        send(ser, 'LY MAX',   1.8, 0.1)
        send(ser, 'Button A', 0.1, 0.2) # 「本体」
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'Button A', 0.1, 0.2) # 「日付と時刻」
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'Button A', 0.1, 0.2) # 「現在の日付と時刻」
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LY MIN',   0.05, 0.05) # 1日進める
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LY MIN',   0.05, 0.05) # 1分進める
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'Button A', 0.1, 0.2) # OK

        send(ser, 'Button HOME', 0.1, 0.5)
        send(ser, 'Button HOME', 0.1, 0.5) # ゲームに戻る

        # idkuji.idkuji(ser)

        send(ser, 'Button A', 0.1, 0.2) # ロトミにアクセス
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'Button A', 0.1, 3.0) # ポケジョブを開く
        send(ser, 'Button A', 0.1, 0.4) # 新しいジョブがあります
        print("おかえりムービー")
        send(ser, 'Button A', 0.1, 13.0)
        send(ser, 'Button A', 0.1, 0.5)
        send(ser, 'Button A', 0.1, 0.5)
        send(ser, 'Button A', 0.1, 2.6)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button B', 0.1, 0.6) # 閉じる
        send(ser, 'Button A', 0.1, 0.4)

        cnt += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("Start")
        print("育成するポケモンの数 > ", end="")
        poke = int(input())
        print("育成する日数 > ", end="")
        day = int(input())
        send(ser, 'Button B', 0.1, 0.5)
        pokejob(ser, poke, day)

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        print("End.")
        ser.close()
