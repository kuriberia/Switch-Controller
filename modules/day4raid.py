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

def day(ser):
    send(ser, 'Button A', 0.1, 0.4) # 巣穴を見る
    send(ser, 'Button A', 0.1, 2.7) # みんなで挑戦を選択
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
    send(ser, 'LX MAX',   0.05, 0.05)
    send(ser, 'Button A', 0.1, 0.2) # OK

    send(ser, 'Button HOME', 0.1, 0.5)
    send(ser, 'Button HOME', 0.1, 0.5) # ゲームに戻る
    send(ser, 'Button B', 0.1, 0.6)
    send(ser, 'Button A', 0.1, 4.2) # 募集をやめる
    send(ser, 'Button A', 0.1, 0.3) # ワット回収 「巣穴からエネルギーが少しだけでている！▼」
    send(ser, 'Button B', 0.1, 0.3) # 「シベリアは1000W手に入れた！▼」

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default="/dev/ttyS7")
    parser.add_argument('-d', '--day', type=int, default=3)
    args = parser.parse_args()
    ser = serial.Serial(args.port, 9600)
    try:
        print("Start")
        send(ser, 'Button B', 0.1, 0.5)
        send(ser, 'Button R', 0.1, 0.5)

        day(ser)
        send(ser, 'Button B', 0.1, 1.0) # ダイアログを閉じる
        send(ser, 'Button B', 0.1, 1.0) # レイドを閉じる

    except KeyboardInterrupt:
        send(ser, 'RELEASE')
        print("End.")
        ser.close()
